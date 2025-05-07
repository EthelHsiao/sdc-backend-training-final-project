# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安裝poetry
RUN pip install poetry

# 複製配置文件
COPY pyproject.toml poetry.lock* /app/

# 配置poetry不建立虛擬環境
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root


# 複製應用程序代碼
COPY app /app/app

# 設置環境變量
ENV OLLAMA_URL=http://ollama:11434/api/chat
ENV DATABASE_URL=sqlite:///./data/app.db

# 創建數據目錄
RUN mkdir -p /app/data

# 暴露API端口
EXPOSE 8000

# 運行應用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]