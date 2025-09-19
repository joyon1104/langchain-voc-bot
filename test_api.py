import requests
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def test_chat_completion():
    # .env 파일에서 포트 읽기 (기본값: 8000)
    port = os.getenv('API_PORT', '8000')
    url = f"http://localhost:{port}/analyze_voc"
    print(f"테스트 URL: {url}")
    
    # 테스트할 프롬프트들
    test_prompts = [
        "서비스에서 Chat 기능에 대한 사용법을 알려줄래?",
        "서비스를 설치하는데 오류가 발생했어. 어떻게 해결하지?",
        "토큰 생성하는 홈페이지에 로그인할 수 없어. 도와줄 수 있니?",
    ]
    
    for prompt in test_prompts:
        payload = {
            "prompt": prompt
        }
        
        try:
            # API 호출
            response = requests.post(url, json=payload)
            
            # 결과 출력
            print(f"\n테스트 프롬프트: {prompt}")
            print(f"상태 코드: {response.status_code}")
            print(f"응답 결과: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
        except requests.exceptions.ConnectionError as e:
            print(f"\n연결 에러 발생: {e}")
            print(f"FastAPI 서버가 {url}에서 실행 중인지 확인해주세요.")
            break
        except Exception as e:
            print(f"\n예상치 못한 에러 발생: {e}")
            break

if __name__ == "__main__":
    test_chat_completion()
