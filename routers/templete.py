# 对外模版
def get_template(gameName, gameDescribe, gameFeature, keywords, language, style, total_character):
    kw_list = []
    has_keyword = """
    I will provide you with some keywords that are very important to me. If they are not included in the article, it will be a very poor article. Please think step by step and make sure to include all of the keywords I provided in the copy. You don’t need to worry about the grammatical structure, context, or spelling of the words.The keywords are very important, so please make sure to include all of them. The important keywords are: 
    """
    has_keyword2 = """
    After you generate the copy according to the above requirements, expand the copy based on the following keywords. The keywords should not appear consecutively. Please don’t miss the keywords I gave you:
    """
    if len(keywords) != 0:
        #拼接keywords至单kw_list
        for i in keywords:
            times = i.times
            keyword = [i.keyword]
            tmp = keyword * times
            kw_list = kw_list + tmp
            tmp = []
            # logging.info(kw_list)
        if len(kw_list) !=0:
            key_word = kw_list
    else:
        key_word = ""
        has_keyword = "" 
        has_keyword2 = ""
    templates = [
        f"""
        I need you to act as an advertiser and help me write a promotional copy for the {gameName} game. The language used for the promotional copy is {language}.
        {has_keyword}{keywords}
        The gameplay and features of the game is as follows:Gameplay: {gameDescribe}, Game features: {gameFeature}. You need to expand them into a perfect promotional copy without losing the gameplay and features I provide.
        The promotional copy should meet the following format requirements:
        Add emojis at appropriate positions in the copy, but do not use too many emojis in the same place.
        Start by giving an overview and using category words to highlight the game's features and attract players' interest and participation.
        "How to play": Provide a brief introduction to the game's gameplay.
        "Game Features": List the game's features and let players experience the fun of the game.
        Finally, conclude by calling for downloads and encouraging players to enjoy the fun of the game with interesting language.
        {has_keyword2}{key_word}
        The total characters requirement are {total_character} characters, with a total character count that can fluctuate up or down by 10% or 200 characters.
        When you finish,double-check the passage to ensure that each keyword appears exactly the number of times I want and that means none of the keywords appears more or less than I want.
        Please be very careful, please use {language} for the full text, do not use other languages.
        """,
        f"""
        I need you to act as an advertiser and help me write a promotional copy for the {gameName} game. The language used for the promotional copy is {language}.
        {has_keyword}{keywords}
        I will provide you with the gameplay and features of the game, and you need to expand them into a perfect promotional copy without losing the gameplay and features I provide.Gameplay: {gameDescribe}, Game features: {gameFeature}.
        The copy should be continuous and have a storytelling feel. The total number of paragraphs should not be less than 5, and please do not add emojis. 
        Copywriting requirements: 1. The first paragraph should be an overview, providing keywords, briefly pointing out the game's features, and arousing players' interest and desire to participate. 2. The gameplay and content should be progressively distributed throughout the paragraphs, with the overall copy being relatively long. 
        {has_keyword2}{keywords}
        The total characters requirement are {total_character} characters, with a total character count that can fluctuate up or down by 10% or 200 characters.
        When you finish,double-check the passage to ensure that each keyword appears exactly the number of times I want and that means none of the keywords appears more or less than I want.
        Please be very careful, please use {language} for the full text, do not use other languages.
        """,
        f"""
        I need you to act as an advertiser and help me write a promotional copy for the {gameName} game. The language used for the promotional copy is {language}.
        I will provide you with the gameplay and game features, and the completion you generate needs to include the gameplay and game features I provided you. Gameplay: {gameDescribe}; Game Features :{gameFeature}
        {has_keyword}{keywords}
        Copywriting requirements:
        Copy requirements:First, briefly introduce the game to arouse players' interest and desire to participateThen introduce the content of each module of the game, summarizing the content of each module with a title in uppercase letters, please do not use the word 'module' in the title，and starting a new line for the specific content.Finally, summarize the game's features and use provocative language to attract players to download the game.
        {has_keyword2}{keywords}
        The total characters requirement are {total_character} characters, with a total character count that can fluctuate up or down by 10% or 200 characters.
        When you finish,double-check the passage to ensure that each keyword appears exactly the number of times I want and that means none of the keywords appears more or less than I want.
        Please be very careful, please use {language} for the full text, do not use other languages.
        """,
        f"""
        I need you to act as an advertiser and help me write a promotional copy for the {gameName} app. The language used for the promotional copy is {language}.
        I will provide you with the gameplay and game features, and the completion you generate needs to include the gameplay and game features I provided you. Gameplay: {gameDescribe}; Game Features :{gameFeature}
        {has_keyword}: {keywords}.
        Copywriting Requirements:
        The first paragraph should start with the app name or an important keyword related to the app. It should use provocative language, such as exclamatory or interrogative sentences, to attract user interest and encourage participation.
        Next, introduce the app's features and how they meet users' needs.
        Briefly list the app's unique features, with each feature on a separate line and described in a sentence, phrase, or keyword.
        Describe the app's main special features, with each feature having a title line that summarizes its content in all capital letters within 【】,and starting a new line for the specific content.Each special feature should have a separate paragraph for its detailed introduction.
        Finally, summarize the app and encourage users to download it.
        Add emojis at appropriate positions in the copy, but do not use too many emojis in the same place.
        {has_keyword2}{keywords}
        The total characters requirement are {total_character} characters, with a total character count that can fluctuate up or down by 10% or 200 characters.
        When you finish,double-check the passage to ensure that each keyword appears exactly the number of times I want and that means none of the keywords appears more or less than I want.
        Please be very careful, please use {language} for the full text, do not use other languages.
        """,
        f"""
        I need you to act as an advertiser and help me write a promotional copy for the {gameName} app. The language used for the promotional copy is {language}.Add emojis at appropriate positions in the copy, but do not use too many emojis in the same place.
        I will provide you with the application description and features. Your generated copy should include the description and features of the application I have provided. The application description is {gameDescribe}, and the application features are {gameFeature}.
        {has_keyword} {keywords}.
        Requirements for the copy:
        In the first paragraph, start with the name of the application or an important keyword of the application, and use provocative language, such as exclamatory or interrogative sentences, to attract the user's interest and desire to participate.
        Then introduce what kind of function the application product can help the user achieve and what kind of needs it can meet.
        Briefly list the functional features of the application, each feature on a separate line, expressed in a sentence, phrase, or keyword.
        In the form of a numerical serial number, the operation steps of the APP are introduced in detail
        Use more specific descriptions to introduce the main featured functions of the application. This part requires more detailed expansion based on the application features I provided to you, with a detailed description of each featured function consisting of no less than three sentences. Each unique feature with a title line that summarizes the content in square brackets【】, with all English letters capitalized. Each unique feature title is on a separate line, and the specific feature description is in a separate paragraph.
        Finally, indicate that more features are under development, and stay tuned!
        {has_keyword2}{keywords}
        The total characters requirement are {total_character} characters, with a total character count that can fluctuate up or down by 10% or 200 characters.
        Please be very careful, please use {language} for the full text, do not use other languages.
        """
    ]  
    prompt = templates[style]
    return prompt



# 对内模版
def get_template_inner(gameName, gameDescribe, gameFeature, keywords, language, style, total_character, emoji):
    
    # 文案生成长度默认为1000
    if language.lower() in ["japanese", "chinese", "korean"]:
        if total_character == 1000:
            total_character = 2500
        else:
            total_character = 5000
    else:
        if total_character == 1000:
            total_character = 450
        else:
            total_character = 8000




    # if total_character == "":
    #     total_character = 1200
    # else:
    #     if total_character == 1000:
    #         total_character = 1200
    #     else:
    #         total_character = 4000

    # 默认没有emoji
    if emoji == "":
        emojis = "DO NOT contain any emojis."
    else:
        if emoji == 0:
            emojis = "DO NOT contain any emojis."
        else:
            emojis = "Make sure to conclude suitable emojis. Emojis should be added APPROPRIATELY throughout the copy, avoiding excessive usage in a single location."

  
    kw_list = []

    # has_keyword = f"""
    #     Keywords in <> need to be inserted. After you generate the copy according to the above requirements, expand the copy based on the following keywords. Please think the keywords word by word and make sure to include all of the keywords I provided in the <>. Do not change the form of keywords, such as singular, plural, tense, etc. No matter of the grammar, spelling, or any mistake. The keywords are very important, so please make sure to include all of them. 
    #     """

    has_keyword = f"""
    Keywords need to be inserted. After you generate the copy according to the above requirements, expand the copy based on the following keywords. Please think the keywords word by word and make sure to include all of the keywords I provided below. Do not change the form of keywords, such as singular, plural, tense, etc. No matter of the grammar, spelling, or any mistake. The keywords are very important, so please make sure to include all of them. 
    """
    
    # language_en = f"""
    # Create a description in {language} language with approximately {total_character} characters. 
    # """
        
    # language_ja = f"""
    # おおよそ{total_character}文字の{language}言語で記述を作成します。
    # """
    important_advice_en = f"""
        Important advice: 
        Before you output, please Double-check that the CHARACTER COUNT is approximately {total_character}. If not, please think a bit time and then expand the paragraphs, otherwise should not generate the text.
        Please think twice and check whether the above requirements are met (especially the number of characters), and don't care about the time limit for output.
        """

    important_advice_ja = f"""
        重要アドバイス-
        出力する前に、文字数がおおよそ{total_character}であることを再確認してください。そうでない場合は、少し時間を考えてから段落を展開してください、それ以外の場合は、テキストを生成しないでください。
        上記の要件(特に文字数)を満たしているかどうか、出力の制限時間は気にしないでよく考えて確認してください。
        """

    important_advice_zh = f"""
        重要的建议:
        在输出之前，请仔细检查字符计数是否接近于{total_character}。如果没有，请再考虑一下，然后适当扩展段落，达到要求的字符数，否则不应该生成文本。
        请三思，检查是否满足上述要求(特别是字符数)。
        """


    basic_info_en = f"""      
        I need your help as an advertiser to craft a promotional description for the game {gameName}.

        Here are the requirements (ordered by importance):
        1. Create a description in {language} language with approximately {total_character} characters. 
        2. Follow the given format (see below).
        3. Expand the content in ``` to create a captivating promotional description.
        4. {has_keyword}
        5. Ensure the total character count is around {total_character}, with a permissible variation of plus/minus 100 characters.Do not exceed this word limit, this is very important!
        6. Verify that the generated text meets the requirements; if not, please regenerate
        7. Do not generate markdown formatted text

        Basic information of the game: 
        Gameplay: ```{gameDescribe}```
        Game features: ```{gameFeature}```
        Keywords: {keywords}
        """

    basic_info_ja = f"""
        {gameName}ゲームのプロモーション説明を作成する広告主としてあなたの助けを必要としています。

        以下が要件(重要度順)だ:
        1.  おおよそ{total_character}文字の{language}言語で記述を作成します。
        2.  与えられたフォーマットに従います(下記参照)。
        3.  ```のコンテンツを展開して、魅力的なプロモーション説明を作成します。
        4.  {has_keyword}
        5.  合計文字数が{total_character}前後であることを確認し、プラス/マイナス100文字のバリエーションが許容されます。Do not exceed this word limit, this is very important!
        6.  生成されたテキストが要件を満たしていることを確認する。そうでない場合は再生してください
        7. markdown 形式のテキストを生成しません。

        ゲームの基本情報:
        游びやすくなった本```{gameDescribe}```
        ゲーム机能:```{gameFeature}```
        关键字:{keywords}
        """
    

    basic_info_zh = f"""  
        请你作为游戏发布者，精心创作一个{gameName}游戏的商店页描述。

        以下是要求(按重要性排序):
        1. 全文用{language} 撰写这个商店页描述，文章内容在{total_character}个字符左右，允许上下浮动100字符。
        2. 遵循给定的格式(见下面)。
        3. 扩展```中的内容，创建一个吸引人的商店页游戏描述。
        4. {has_keyword}
        5. 再次确认总字符数在{total_character}左右，允许上下浮动100字符。
        6. 验证生成的文本是否符合要求；如果没有，请重新生成
        7. 不要生成markdown格式的文本

        游戏基本信息:
        游戏:```{gameDescribe}```
        游戏功能:```{gameFeature}```
        关键词:{keywords}
        """



    if language.lower() in ["japanese", "ja", "日本語"]:
        basic_info = basic_info_ja
        important_advice = important_advice_ja
    elif language.lower() == "chinese":
        basic_info = basic_info_zh
        important_advice = important_advice_zh
    else:
        basic_info = basic_info_en
        important_advice = important_advice_en

    # has_keyword2 = """
    # After you generate the copy according to the above requirements, expand the copy based on the following keywords. The keywords should not appear consecutively. Please don’t miss the keywords I gave you:
    # """
    if len(keywords) != 0:
        #拼接keywords至单kw_list
        for i in keywords:
            times = i.times
            keyword = [i.keyword]
            tmp = keyword * times
            kw_list = kw_list + tmp
            tmp = []
            # logging.info(kw_list)
        if len(kw_list) !=0:
            key_word = kw_list
    else:
        key_word = ""
        has_keyword = "" 
      
    templates = [
        f"""
        {basic_info}

        Format requirements:
        The description ONLY contains FOUR PARTS in {language} language.
        {emojis}
        Begin with an enticing overview, highlighting the game's features and captivating players' interest and engagement.
        "How to play": Introduce how to play the game. You can expend the Gameplay (which in ```) based on your historical experience on the same game. 
        "Game Features": BULLET List the game's features, allowing players to experience the game's enjoyment.
        Finally, conclude by urging downloads and encouraging players to revel in the game's entertainment with captivating language.

        {important_advice}
        """,
        f"""
        {basic_info}

        Format requirements:
        The copy should be continuous and have a storytelling feel. The total number of paragraphs should not be less than 5 and in {language} language. 
        {emojis}
        The first paragraph should be an overview, providing keywords, briefly pointing out the game's features, and arousing players' interest and desire to participate. 
        The gameplay and content should be progressively distributed throughout the paragraphs. 
        
        {important_advice}
        """,
        f"""
        {basic_info}

        Format requirements:
        {emojis}  and in {language} language.
        First, briefly introduce the game to arouse players' interest and desire to participateThen introduce the content of each module of the game, summarizing the content of each module with a title in uppercase letters, please do not use the word 'module' in the title, and starting a new line for the specific content.
        Finally, summarize the game's features and use provocative language to attract players to download the game.

        {important_advice}
        """,
        f"""
        {basic_info}

        Format requirements:
        The whole passage should be shown in {language} language
        The first paragraph should start with the app name or an important keyword related to the app. It should use provocative language, such as exclamatory or interrogative sentences, to attract user interest and encourage participation.
        Next, introduce the app's features and how they meet users' needs.
        Briefly list the app's unique features, with each feature on a separate line and described in a sentence, phrase, or keyword.
        Describe the app's main special features, with each feature having a title line that summarizes its content in all capital letters within 【】,and starting a new line for the specific content.Each special feature should have a separate paragraph for its detailed introduction.
        Finally, summarize the app and encourage users to download it.
        {emojis}

        {important_advice}
        """,
        f"""
        {basic_info}

        Format requirements:
        In the first paragraph, start with the name of the application or an important keyword of the application, and use provocative language, such as exclamatory or interrogative sentences, to attract the user's interest and desire to participate.
        Then introduce what kind of function the application product can help the user achieve and what kind of needs it can meet.
        Briefly list the functional features of the application, each feature on a separate line, expressed in a sentence, phrase, or keyword.
        In the form of a numerical serial number, the operation steps of the APP are introduced in detail
        Use more specific descriptions to introduce the main featured functions of the application. This part requires more detailed expansion based on the application features I provided to you, with a detailed description of each featured function consisting of no less than three sentences. Each unique feature with a title line that summarizes the content in square brackets【】, with all English letters capitalized. Each unique feature title is on a separate line, and the specific feature description is in a separate paragraph.
        Finally, indicate that more features are under development, and stay tuned!
        {emojis}
      
        {important_advice}
        """
    ]  
    prompt = templates[style]
    return prompt


def get_confidence_template_inner(generated_aso_text):


    {}