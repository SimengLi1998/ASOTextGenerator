from fastapi import APIRouter, BackgroundTasks, Body, Response, Request, Header
import asyncio
from aiohttp import ClientSession
import requests
from sse_starlette.sse import EventSourceResponse
from datamodel.aso_model import *
from datamodel.custom_error import *
from routers.templete import *

import openai
import json
import os
import logging
import configparser
import os
from  routers.api_requestor import APIRequestor
import threading

import concurrent.futures
import multiprocessing


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

serviceRouter = APIRouter()

#——————————ASO生成服务 (DBT服务：对外)——————————
#请求azure云, json返回
def request_azurre(prompt, config):
    
    openai.api_type = config['api_type']
    openai.api_version = config['api_version']
    openai.api_base = config['api_base']
    openai.api_key = config['api_key']
    
    messages = []
    messages.append({"role": config['role'], "content": prompt})

    reply = openai.ChatCompletion.create(
            engine=config['gpt35'],
            messages=messages,
            # temperature=0.00001,
            # top_p=0.00000001,
            max_tokens = int(config['output_token'])
        )
    result = reply.get("choices")[0].get("message").get("content")
    return result

#生成的文本关键词个数统计
def search_keywords(keywords, text):
    result = {}
    for i in keywords:
        # 统计子字符串出现次数
        count = text.count(i)
        result[i] = count
    return result

#ASO生成服务 
@serviceRouter.post("/aso",  tags=["aso_generation"], response_model=PromptModel)
async def aso_gc(inputs:AsoInput):
        
    #获取当前文件的的绝对路径
    folder_dir = os.path.dirname(os.path.realpath('__file__'))
    conf = configparser.ConfigParser()
    conf.read(f'{folder_dir}/config.conf')
    dev_mode = os.environ['dev_mode']
    # logging.info(f"dev_mode: {dev_mode}")
    config = conf[dev_mode] #测试
    
    gameName = inputs.gameName
    gameDescribe = inputs.gameDescribe
    gameFeature = inputs.gameFeature
    keywords = inputs.keywords
    language = inputs.language
    style = inputs.style
    total_character = int(config['output_character'])
    
    prompt = get_template(gameName, gameDescribe, gameFeature, keywords, language, style, total_character)
    result = request_azurre(prompt, config)
    
    # 返回生成的内容
    return {"content": result}

#ASO生成服务 
@serviceRouter.post("/aso_stream",  tags=["aso_generation_stream"])
async def aso_gc_stream(inputs:AsoInput):

    #获取当前文件的的绝对路径
    folder_dir = os.path.dirname(os.path.realpath('__file__'))
    conf = configparser.ConfigParser()
    conf.read(f'{folder_dir}/config.conf')
    dev_mode = os.environ['dev_mode']
    config = conf[dev_mode]
    
    gameName = inputs.gameName
    gameDescribe = inputs.gameDescribe
    gameFeature = inputs.gameFeature
    keywords = inputs.keywords
    language = inputs.language
    style = inputs.style
    total_character = int(config['output_character'])
    
    prompt = get_template(gameName, gameDescribe, gameFeature, keywords, language, style, total_character)
    
    #请求azure云, json返回, 如果使用流式响应必须使用同步方法, 因为SSE需要保持连接
    def request_azurre_stream(prompt, config):
        
        openai.api_type = config['api_type']
        openai.api_version = config['api_version']
        openai.api_base = config['api_base']
        openai.api_key = config['api_key']
        
        messages = []
        messages.append({"role": config['role'], "content": prompt})

        response = openai.ChatCompletion.create(
                engine=config['gpt35'],
                messages=messages,
                # temperature=0.00001,
                # top_p=0.00000001,
                max_tokens = int(config['output_token']),
                stream = True
            )
        
        for line in response:
            
            if line:
                if line.get("choices")[0]:
                    if line.get("choices")[0].get("delta"):
                        if line.get("choices")[0].get("delta").get("content"):
                            data = line.get("choices")[0].get("delta").get("content")
                            yield data
                            
    # 返回生成的内容
    return EventSourceResponse(request_azurre_stream(prompt, config))

#ASO生成服务 
@serviceRouter.post("/aso_dbtstream",  tags=["aso_generation_dbtstream"])
async def aso_gc_stream(inputs:AsoInput):

    import configparser
    import os
    from routers.templete import get_template

    #获取当前文件的的绝对路径
    folder_dir = os.path.dirname(os.path.realpath('__file__'))
    conf = configparser.ConfigParser()
    conf.read(f'{folder_dir}/config.conf')
    dev_mode = os.environ['dev_mode']
    config = conf[dev_mode]
    
    gameName = inputs.gameName
    gameDescribe = inputs.gameDescribe
    gameFeature = inputs.gameFeature
    keywords = inputs.keywords
    language = inputs.language
    style = inputs.style
    total_character = int(config['output_character'])
    
    prompt = get_template(gameName, gameDescribe, gameFeature, keywords, language, style, total_character)

    #调用公司服务
    # def post_dbtservice(prompt, config):
    #     headers = {'Content-Type': 'application/json', 'charset':'utf-8', 'X-Request-req-accessKeyId': 'a2fhn1t7mnbs80765ork9hha', 'X-Request-req-token': 'zvmh5lgok65qs53r8ifwxtlz'}
    #     data = {'issue': prompt, 'maxPromptToken': int(config['output_token'])}
    #     response = requests.post(f"https://openapi-pre.uqualities.com/AIGCChatGptServ/saas/{config['model']}/stream", headers=headers, data=json.dumps(data))
    #     _byte_list = []
    #     for line in response:
    #         sline = str(line)
    #         if sline.match("data:(.*?)/n/n")
            
    #         yield line
    
    def post_dbtservice(prompt, config):
        requestor = APIRequestor(
            
        )
        data = {'issue': prompt, 'maxPromptToken': int(config['output_token'])}
        response, _ = requestor.request(
            "post",
            f"{config['url']}/AIGCChatOpenServ/saas/{config['model']}/stream",
            params=data,
            headers = {'Content-Type': 'application/json', 'charset':'utf-8', "X-Request-req-accessKeyId": config['aso_accessKeyId'], 'X-Request-Req-Accesskeysecret': config['aso_accessKeySecret']},
            stream=True
        )
        # print(response.data)
        for line in response:
            if line.data:
                if line.data.get('data'):
                    if line.data.get('data').get('answer'):
                        yield line.data.get('data').get('answer')
    
    return EventSourceResponse(post_dbtservice(prompt, config))





#——————————ASO生成服务 (DBT服务：对内)——————————

#ASO生成服务 (DBT服务：对内)
@serviceRouter.post("/aso_dbtstream_inner",  tags=["aso_generation_dbtstream_inner"])
async def aso_gc_stream(inputs:AsoInputInner):
    # print("/aso_dbtstream_inner打印")
    import configparser
    import os
    import requests

    #获取当前文件的的绝对路径
    folder_dir = os.path.dirname(os.path.realpath('__file__'))
    conf = configparser.ConfigParser()
    conf.read(f'{folder_dir}/config.conf')
    dev_mode = os.environ['dev_mode']
    config = conf[dev_mode]
    
    gameName = inputs.gameName
    gameDescribe = inputs.gameDescribe
    gameFeature = inputs.gameFeature
    keywords = inputs.keywords
    language = inputs.language
    style = inputs.style
    emoji = inputs.emoji
    # total_character = int(config['output_character']) #默认1000
    total_character = inputs.total_character
    
    prompt = get_template_inner(gameName, gameDescribe, gameFeature, keywords, language, style, total_character, emoji)
    # print(prompt)

    # 非流式输出
    # def post_dbtservice(prompt, config):
    #     # print(prompt)
    #     data = {'issue': prompt, 'maxPromptToken': int(config['output_token'])}
    #     headers = {'Content-Type': 'application/json', 'charset':'utf-8', "X-Request-req-accessKeyId": config['cp_accessKeyId'], 'X-Request-Req-Accesskeysecret': config['cp_accessKeySecret']}
    #     response = requests.post(f"{config['url']}/AIGCChatOpenServ/saas/{config['model']}/text", json=data, headers = headers)
    #     # print(response.text)
    #     return response.text
    # response = post_dbtservice(prompt, config)
    # # print(prompt)
    # # print(response)
    # return response

     
    # 流式输出
    def post_dbtservice(prompt, config):
        requestor = APIRequestor(
            
        )
        data = {'issue': prompt, 'maxPromptToken': int(config['output_token'])}
        response, _ = requestor.request(
            "post",
            f"{config['url']}/AIGCChatOpenServ/saas/{config['model']}/stream", # 流式输出

            params=data,
            headers = {'Content-Type': 'application/json', 'charset':'utf-8', "X-Request-req-accessKeyId": config['aso_accessKeyId'], 'X-Request-Req-Accesskeysecret': config['aso_accessKeySecret']},
            stream=True
        )
        for line in response:
            if line.data:
                if line.data.get('data'):
                    if line.data.get('data').get('answer'):
                        yield line.data.get('data').get('answer')
    
    return EventSourceResponse(post_dbtservice(prompt, config))


#————————————ASO文案分类服务————————————

# 文案分类
import traceback
import json
from typing import Dict, Any, List
# @serviceRouter.post("/classify", response_model=List[Dict[str, Any]])
@serviceRouter.post("/classify")
async def call_overseas_server(text_content:TextContent):
    import requests

    folder_dir = os.path.dirname(os.path.realpath('__file__'))
    config = configparser.ConfigParser()
    config.read(f'{folder_dir}/config.conf')
    overseas_server_url = config.get("oversea", "overseas_server_url")
    # overseas_server_url = "http://43.153.94.214:8000/service/classify"

    payload = {"text": text_content.text}
    response = requests.post(overseas_server_url, json=payload)

    # response = str(response).replace("[","").replace("]","")
    json_response = json.loads(response.text)
    print(json_response)
    return json_response



# # 文案分类(高并发，待完善)
# import asyncio
# import requests
# from typing import Dict, Any, List

# # @serviceRouter.post("/classify", response_model=List[Dict[str, Any]])
# @serviceRouter.post("/classify")
# async def call_overseas_server(text_content: TextContent):


#     overseas_server_url = "http://43.153.94.214:8000/service/classify"
#     payload = {"text": text_content.text}

#     async def send_request(url, data):
#         response = await loop.run_in_executor(None, requests.post, url, data)
#         return response.text

#     try:
#         loop = asyncio.get_event_loop()
#         response_text = await send_request(overseas_server_url, payload)
#         return response_text
#     except Exception as e:
#         traceback.print_exc()
#         return {"error": str(e)}





#————————————code生成服务————————————


@serviceRouter.post("/code_dbtstream",  tags=["code_generation_dbtstream"])
# async def code_generator(inputs: CodeInput = Body(embed=True)):
async def code_generator(inputs: CodeInput, background_tasks: BackgroundTasks):
    
    #接收信息后立即返回接收成功信息
    
    
    #获取当前文件的的绝对路径
    folder_dir = os.path.dirname(os.path.realpath('__file__'))
    conf = configparser.ConfigParser()
    conf.read(f'{folder_dir}/config.conf')
    dev_mode = os.environ['dev_mode']
    # logging.info(f"dev_mode: {dev_mode}")
    config = conf[dev_mode] #测试
    
    role = "你扮演一个高级软件工程师角色,你需要仔细并严格遵循用户的要求,逐步思考用户给你的用户给你的描述.尽量减少任何其他的散文."
    content_list = [] 
    cores = multiprocessing.cpu_count() #获取本机CPU核数
    results = [] #保存各个进程执行结果
    
    #同步请求chatgpt的方法
    def req_gpt(segment):
        retry_count = 3 #设置重试次数
        prompt = f""""请用{inputs.code_language}帮我写代码,确保你写的代码可以运行。你只需要提供我唯一的代码块即可,不要给我提供你的代码思路！
                    代码描述为：{segment.scene_describe}。
                    代码要求:
                    1.描述中涉及数据信息的需求,代码需要合理帮我实现获取和存储更新当前数据、信息、状态的方法。
                    2.对于逻辑描述不全的,代码需要自动帮我完善逻辑。
                    3.代码要写得非常详细,在单一的代码块中输出代码,代码在300行左右。
                    4.只输出代码和代码注释,不输出内容解释。
                    请必须注意:代码中的TODO部分需要你根据常见方法或逻辑帮我填入代码,我不希望在你提供的代码有看到TODO需要我自己填写相应逻辑的,这种我是不接受的。  
                """

        headers = {'Content-Type': 'application/json', 'charset':'utf-8', "X-Request-req-accessKeyId": config['cp_accessKeyId'], 'X-Request-Req-Accesskeysecret': config['cp_accessKeySecret']}
        data = {'issue': prompt, 'systemContent': role,'maxPromptToken': int(config['max_token'])}
        while retry_count > 0:
            try:
                response = requests.post(f"{config['url']}/AIGCChatOpenServ/saas/{config['model']}/text", headers=headers, data=json.dumps(data))
                cont1 = json.loads(response.content)
                print(f"text: {cont1}")
                text = cont1['data']['answer']
                print(f"text1: {text}")
                # 补充伪代码
                prompt2 = f""""请你仔细阅读我提供给你的代码,将代码注释为TODO的伪代码根据注释补充完整,将只有注释没有执行方法的代码框架补充完整,补充的代码和原代码形成完整的唯一一个代码块。只输出代码和代码注释,不输出内容解释。
                            我给你提供的代码为:{text}
                        """
                data2 = {'issue': prompt2, 'systemContent': role, 'maxPromptToken': int(config['max_token'])}
                response = requests.post(f"{config['url']}/AIGCChatOpenServ/saas/{config['model']}/text", headers=headers, data=json.dumps(data2))
                print(f"完成一次请求")
                cont2 = json.loads(response.content)
                text2 = cont2['data']['answer']
                text2 = text2.replace("TODO", "").replace("示例", "").replace("代码", "")
                obj = {"sid": segment.sid, "scene_text": segment.scene_text, "code": text2}
            except Exception as e:
                logging.info('请求失败, 重试请求')
                retry_count -= 1
            else: #无异常则结束重试
                break    
            
            if retry_count == 0:
                logging.info('超出最大重试请求数!')
                raise ExceedMaxRetryError("超出最大重试请求数!")
            
        return obj
    
    # for segment in inputs.scene_list:
    #     job=executor.submit(req_gpt,arg_list[k])
    #     content_list.append(obj)
    # print(content_list)
    
    # async def run_tasks(config, inputs, content_list):
    #     print(f"执行并发请求")
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=cores-1) as executor:
    #         loop = asyncio.get_running_loop()
    #         tasks = [loop.run_until_complete(executor, req_gpt, s) for s in inputs.scene_list]
    #         # results = await [pool.submit(req_gpt, segment) for segment in inputs.scene_list]
    #         # for future in concurrent.futures.as_completed(results):
    #         #     # print(future.result())
    #         #     content_list.append(future.result())
    #         done, _ = await asyncio.wait(tasks)
    #         content_list = [t.result() for t in done]
    #         return content_list
        
    # content_list = await run_tasks(config, inputs, content_list)
    # #回调入库
    # url = config['callback_url']
    # data = {"task_id": inputs.task_id, "code_language":inputs.code_language, "scene_list": content_list}
    # print(f"开始执行回调~!")
    # # async with aiohttp.ClientSession() as session:
    # #     async with session.post(url, data=data) as response:
    # #         response_data = await response.json()
    # response = requests.post(url, json=data)
    # print(f"执行回调完毕~!")
    
    
    
    #计算代码行数
    # code_lines = len(text2.splitlines())
    # # 去掉每行的首尾空格和注释
    # lines = text2.splitlines()
    # lines = [line.strip() for line in lines]
    # lines = [line for line in lines if line and not line.startswith('//')]
    # code_lines = len(lines)

    # print(f"text2: {text2}")
    # background_tasks.add_task(multi_request(config, inputs, content_list))
    
    
    #异步多线程改异步协程
    async def async_task(prompt):
        logging.info('开启协程')
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await asyncio.get_event_loop().run_in_executor(
                pool,
                req_gpt,
                prompt
            )
        return result
    
    #异步协程并发请求
    async def multi_request(inputs: str):
        logging.info('开启异步多协程请求')
        loop = asyncio.get_running_loop()
        tasks = []
        for prompt in inputs.scene_list:
            tasks.append(asyncio.ensure_future(async_task(prompt)))
        return await asyncio.gather(*tasks)
    
    async def req_callback(config, inputs):
        logging.info('执行回调函数')
        #执行回调操作
        content_list = await multi_request(inputs)
        logging.info(content_list)
        #回调入库
        url = config['callback_url']
        data = json.dumps({"task_id": inputs.task_id, "code_language":inputs.code_language, "scene_list": content_list})
        async with ClientSession() as session:
            async with session.post(url, data=data, headers={'Content-Type': 'application/json', 'charset':'utf-8'}) as response:
                response_data = await response.json()
                logging.info(response_data)
        logging.info('回调函数执行完毕')
    
    # 异步处理其他任务
    asyncio.create_task(req_callback(config, inputs))
    
    return {"status_code": 200, "msg": "请求成功!"}
