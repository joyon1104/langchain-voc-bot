from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from agents.guide_agent import GuideAgent
from agents.issue_agent import IssueAgent

# .env 파일 로드
load_dotenv()

# 환경 변수 확인
if not os.getenv("OPENROUTER_API_KEY"):
    raise ValueError("OPENROUTER_API_KEY 환경 변수가 설정되지 않았습니다.")

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supervisor Agent 구현
class SupervisorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            model_name=os.getenv("OPENROUTER_MODEL")
        )
        template = """다음 사용자의 요청을 분석하여 어떤 에이전트가 처리해야 할지 결정해주세요.
        선택지는 'guide_agent' 또는 'issue_agent' 중 하나여야 합니다.
        guide_agent: 서비스에 대한 일반적인 안내와 도움을 제공하는 에이전트
        issue_agent: 서비스의 문제 해결과 이슈 처리를 담당하는 에이전트
        응답은 선택한 에이전트 이름만 출력해주세요.
        
        사용자 요청: {prompt}
        """
        self.prompt = ChatPromptTemplate.from_template(template)
        self.chain = self.prompt | self.llm
    
    def route_prompt(self, prompt: str) -> str:
        response = self.chain.invoke({"prompt": prompt})
        return response.content.strip()

# Supervisor Agent 인스턴스 생성
supervisor = SupervisorAgent()

# Agent 인스턴스 생성
guide_agent = GuideAgent()
issue_agent = IssueAgent()

@app.get("/")
async def root():
    return {"message": "FastAPI 설치 완료!"}

class CompletionRequest(BaseModel):
    prompt: str

@app.post("/analyze_voc")
async def chat_completion(request: CompletionRequest):
    # Supervisor를 통해 적절한 agent 결정
    assigned_agent = supervisor.route_prompt(request.prompt)
    
    # 해당하는 agent로 요청 처리
    if assigned_agent == "guide_agent":
        response = await guide_agent.process(request.prompt)
    else:
        response = await issue_agent.process(request.prompt)
    
    return {
        "assigned_agent": assigned_agent,
        "response": response
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)