from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

class IssueAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            model_name="openai/gpt-3.5-turbo"
        )
        template = """당신은 문제 해결 전문가입니다.
        사용자가 제시한 문제나 이슈에 대해 명확한 해결책을 제시해주세요.
        
        문제/이슈: {prompt}
        """
        self.prompt = ChatPromptTemplate.from_template(template)
        self.chain = self.prompt | self.llm
    
    async def process(self, prompt: str) -> str:
        response = self.chain.invoke({"prompt": prompt})
        return response.content.strip()
