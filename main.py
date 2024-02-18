from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import questions
import json
import model

app = FastAPI()

origins = [
    "http://3.36.140.169:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory='/root/chatbot_server/front')
app.mount("/js", StaticFiles(directory="/root/chatbot_server/front/js"), name="js")
app.mount("/css", StaticFiles(directory='/root/chatbot_server/front/css'), name='css')
app.mount("/logo", StaticFiles(directory='/root/chatbot_server/front/logo'), name='img')

@app.get('/', response_class=HTMLResponse)
def main_page(request: Request):
	return templates.TemplateResponse('index.html', context={'request':request})

@app.get('/index.html', response_class=HTMLResponse)
def main_page(request: Request):
	return templates.TemplateResponse('index.html', context={'request':request})

@app.get('/mytest.html', response_class=HTMLResponse)
def my_test(request: Request):
	return templates.TemplateResponse('mytest.html', context={'request':request})

@app.get('/middletest.html', response_class=HTMLResponse)
def main_page(request: Request):
	return templates.TemplateResponse('middletest.html', context={'request':request})

@app.get('/yourtest.html', response_class=HTMLResponse)
def your_test(request: Request):
	return templates.TemplateResponse('yourtest.html', context={'request':request})

@app.get('/naming.html', response_class=HTMLResponse)
def main_page(request: Request):
	return templates.TemplateResponse('naming.html', context={'request':request})

@app.get('/birth.html', response_class=HTMLResponse)
def main_page(request: Request):
	return templates.TemplateResponse('birth.html', context={'request':request})

@app.get('/chatting.html', response_class=HTMLResponse,)
def main_page(request: Request):
	return templates.TemplateResponse('chatting.html', context={'request':request})

# question, answer 뽑아오기
@app.post('/mytest.html', response_class=JSONResponse)
async def getFromDB(request: Request):
	list = questions.mongoDB()
	return list

@app.post('/naming.html', response_class=JSONResponse)
async def conversation(request: Request):
	conv = questions.getconv()
	# conv = json.dumps(conv)
	return conv

@app.post('/birth.html', response_class=JSONResponse)
async def getParents(request: Request):
    data = await request.json()  # JSON 형식의 데이터 추출
    print(data['parents'])
    model.Parents(data['parents'])
    return {"message": "Received data successfully"}

@app.post('/chatting.html', response_class=JSONResponse)
async def runModel(request: Request):
    data = await request.json()  # JSON 형식의 데이터 추출
    message = model.getAnswer(data['question'])
    print(data['question'])
    return {"message": message}