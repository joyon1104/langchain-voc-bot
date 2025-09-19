# Langchain VOC bot

## Overview

This project is a FastAPI-based server designed to process and handle Voice of Customer (VOC) feedback efficiently. The system leverages a supervisor-agent architecture where incoming VOC requests are intelligently routed through a supervisor to the most appropriate specialized agent, ensuring optimal and contextually relevant responses.

### Key Features

- **Intelligent Agent Routing**: Supervisor-based system that selects the best agent for each VOC request
- **Specialized Agents**: Multiple dedicated agents for different types of customer inquiries
- **FastAPI Framework**: High-performance, modern web framework with automatic API documentation
- **Scalable Architecture**: Modular design supporting easy addition of new agents and workflows

### Architecture

The system consists of:
- **Supervisor**: Routes incoming VOC requests to appropriate agents
- **Guide Agent**: Handles general guidance and informational queries
- **Issue Agent**: Processes and analyzes customer issues and complaints
- **Workflow Management**: Manages state and processing flow across agents

## Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key (for AI analysis)

### Installation

#### 1. Create Virtual Environment

**Windows:**

```bash
# Install virtualenv (if not already installed)
python -m pip install virtualenv

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**Linux/macOS:**

```bash
# Install virtualenv (if not already installed)
python3 -m pip install virtualenv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
# Make sure virtual environment is activated first
pip install -r requirements.txt
```

#### 3. Configuration

```bash
# 1) Create your local env only once
cp .env.template .env

# 2) Open .env and fill real values
# e.g.
# OPENROUTER_API_KEY=sk-...
# OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
# API_PORT=8000
```

## Usage

### Basic Usage

#### 1. FastAPI 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. FastAPI Docs 확인
FastAPI의 자동 생성된 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs

### Debug

#### 1. .vscode/launch.json 파일 생성 후 아래 내용 추가
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI Server (uvicorn module)",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "{원하는 포트번호}",
                "--reload"
            ],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "envFile": "${workspaceFolder}/.env",
            "python": "${workspaceFolder}/venv/Scripts/python.exe",
            "justMyCode": false
        }
    ]
}
```

#### 2. Debug 실행 (F5키 클릭)

### Test

#### 1. FastAPI 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. teat_api.py 실행
```bash
python test_api.py
```

#### 3. 터미널에서 응답 결과 확인

## Project Structure

```
langchain-voc-bot/
├── .env                          # Environment variables (local)
├── .env.template                 # Environment template file
├── .gitignore                    # Git ignore rules
├── main.py                       # Main FastAPI application
├── README.md                     # Project documentation
├── test_api.py                   # API testing script
└── agents/                       # AI agent modules
    ├── guide_agent.py           # Guide agent implementation
    └── issue_agent.py           # Issue analysis agent
```
