from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

class GuideAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            model_name="openai/gpt-3.5-turbo"
        )
        template = """당신은 친절한 안내 도우미입니다.
        사용자의 질문에 대해 명확하고 상세한 안내를 제공해주세요.
        
        질문: {prompt}
        """
        self.prompt = ChatPromptTemplate.from_template(template)
        self.chain = self.prompt | self.llm
    
    async def process(self, prompt: str) -> str:
        response = self.chain.invoke({"prompt": prompt})
        return response.content.strip()
