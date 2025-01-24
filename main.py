from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import requests
import uvicorn
import logging
import os
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ollama Chat UI",
    description="A web interface for Ollama LLM",
    version="1.0.0"
)

# Create templates and static directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the chat interface"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    """Handle chat requests"""
    try:
        body = await request.json()
        messages = body.get("messages", [])
        model = body.get("model", "deepseek-r1:14b")

        ollama_request = {
            "model": model,
            "messages": messages,
            "stream": True  # Enable streaming
        }

        logger.info(f"Sending to Ollama: {ollama_request}")

        # Create streaming response
        async def generate():
            with requests.post(
                "http://localhost:11434/api/chat",
                json=ollama_request,
                stream=True
            ) as response:
                for line in response.iter_lines():
                    if line:
                        json_response = json.loads(line)
                        if 'message' in json_response:
                            content = json_response['message'].get('content', '')
                            if content:
                                yield f"data: {json.dumps({'content': content})}\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 