import httpx
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")

async def generate(model: str, messages: list[dict], stream: bool = False):
    async with httpx.AsyncClient(timeout=None) as client:
        headers = {
            "Accept": "application/x-ndjson" if stream else "application/json"
        }
        res = await client.post(
            OLLAMA_URL,
            json={"model": model, "messages": messages, "stream": stream},
            headers=headers
        )
        res.raise_for_status()
        return res.content if stream else res.json()
