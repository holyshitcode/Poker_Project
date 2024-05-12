from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os.path

app = FastAPI()

# 정적 파일을 제공할 디렉터리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# 플레이 기록을 파일에서 읽어오는 함수
def history_get(file_path):
    play_history = []
    # 파일이 존재하는지 확인
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split('/')
                if len(parts) == 3:  # 플레이 기록이 세 부분(date, player, result)으로 나뉘어야 함
                    date, player, result = parts
                    play_history.append({"date": date, "player": player, "result": result})
                else:
                    print(f"Ignoring invalid line in file: {line}")
    else:
        print(f"File '{file_path}' does not exist.")
    return play_history

# 루트 경로에 연결된 엔드포인트로 HTML 파일 제공
@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# /rank 엔드포인트에 GET 요청을 처리하는 함수로 수정
@app.get("/rank", response_class=HTMLResponse)
async def give_rank(request: Request):
    # 파일에서 플레이 기록을 가져옴
    history = history_get("./uploads/rank.txt")
    # 템플릿 렌더링 및 응답 생성
    return templates.TemplateResponse("index.html", {"request": request, "history": history})
