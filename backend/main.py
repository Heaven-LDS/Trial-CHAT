from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import httpx
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
logger.info(f"Loading .env from: {env_path}")
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://models.inference.ai.azure.com")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "DeepSeek-V3-0324")

logger.info(f"API Key configured: {bool(OPENAI_API_KEY)}")
logger.info(f"Base URL: {OPENAI_BASE_URL}")
logger.info(f"Model: {OPENAI_MODEL}")

# Rate limiting configuration
RATE_LIMIT_WINDOW = 60  # 60 seconds
MAX_REQUESTS_PER_WINDOW = 1  # GitHub API limit

# Request queue and rate limiter
last_request_time: Optional[datetime] = None
request_queue = asyncio.Queue()
queue_processor_task = None

async def process_queue():
    """Process requests from the queue with rate limiting."""
    global last_request_time

    while True:
        try:
            # Get request from queue
            future, message = await request_queue.get()

            # Check rate limit
            if last_request_time:
                time_since_last = (datetime.now() - last_request_time).total_seconds()
                wait_time = max(0, RATE_LIMIT_WINDOW - time_since_last)

                if wait_time > 0:
                    logger.info(f"Rate limit: waiting {wait_time:.1f}s before next request")
                    await asyncio.sleep(wait_time)

            # Process the request
            last_request_time = datetime.now()
            try:
                result = await call_api(message)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                request_queue.task_done()

        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in queue processor: {e}")

async def call_api(message: str) -> str:
    """Call the GitHub API with the given message."""
    logger.info(f"Calling API: {OPENAI_BASE_URL}/chat/completions")

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ],
            },
        )

        logger.info(f"API response status: {response.status_code}")

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "60"))
            logger.warning(f"Rate limit hit, retrying after {retry_after}s")
            await asyncio.sleep(retry_after)
            # Retry once after waiting
            return await call_api(message)

        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        logger.info(f"Response received, length: {len(reply)}")
        return reply

app = FastAPI(title="ChatGPT-like Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """Start the queue processor when the app starts."""
    global queue_processor_task
    queue_processor_task = asyncio.create_task(process_queue())
    logger.info("Queue processor started")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop the queue processor when the app shuts down."""
    global queue_processor_task
    if queue_processor_task:
        queue_processor_task.cancel()
        try:
            await queue_processor_task
        except asyncio.CancelledError:
            pass
        logger.info("Queue processor stopped")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Chat endpoint.

    - If OPENAI_API_KEY is missing, returns a mock echo response.
    - Otherwise, queues the request and calls GitHub's chat completion API.
    """

    logger.info(f"Received message: {req.message}")
    logger.info(f"Queue size: {request_queue.qsize()}")

    # Mock mode when no API key is configured
    if not OPENAI_API_KEY:
        logger.warning("No API key configured, returning mock response")
        return ChatResponse(reply=f"(mock) You said: {req.message}")

    try:
        # Create a future for this request
        future = asyncio.Future()

        # Add to queue
        await request_queue.put((future, req.message))
        logger.info(f"Added to queue (position: {request_queue.qsize()})")

        # Wait for the result
        reply = await future
        return ChatResponse(reply=reply)

    except asyncio.CancelledError:
        logger.warning("Request cancelled")
        raise HTTPException(status_code=499, detail="Request cancelled")
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

