import os
import requests
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class LLMClient:
    def __init__(self):
        self.llm_server_url = os.getenv("LLM_SERVER_URL")
        if not self.llm_server_url:
            raise ValueError("LLM_SERVER_URL 환경 변수가 설정되지 않았습니다.")
    
    def generate(self, prompt: str, temperature: float = 0, max_tokens: int = 100) -> str:
        """
        자체 LLM 서버에 요청을 보내고 응답을 받습니다.
        
        Args:
            prompt (str): LLM에 보낼 프롬프트
            temperature (float): 생성 온도 (기본값: 0)
            max_tokens (int): 최대 토큰 수 (기본값: 100)
            
        Returns:
            str: LLM의 응답 텍스트
        """
        try:
            payload = {
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                self.llm_server_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # 서버 응답 형식에 따라 조정 필요
                # 일반적인 형태들을 처리
                if "response" in result:
                    return result["response"].strip()
                elif "text" in result:
                    return result["text"].strip()
                elif "content" in result:
                    return result["content"].strip()
                elif "generated_text" in result:
                    return result["generated_text"].strip()
                else:
                    # 응답이 직접 문자열인 경우
                    return str(result).strip()
            else:
                raise Exception(f"LLM 서버 오류: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"LLM 서버 연결 오류: {e}")