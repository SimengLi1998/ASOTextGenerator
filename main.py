from routers import service
from fastapi import FastAPI
import uvicorn
import sys
import os
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

app = FastAPI()
app.include_router(service.serviceRouter,prefix='/service',tags=["service模块"])


if __name__  == '__main__':
    if sys.argv[1]:
        os.environ['dev_mode'] = sys.argv[1]
    else:
        os.environ['dev_mode'] = 'dev'
    logging.info(f"dev_mode: {sys.argv[1]}")
    uvicorn.run('main:app',host='0.0.0.0',port=7805,reload=True, workers=4)
    
    

    





