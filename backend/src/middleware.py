from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from colorama import init, Fore, Style

init()

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def get_method_emoji(method: str) -> str:
    method_emojis = {
        "GET": "🔍",
        "POST": "📝",
        "PUT": "📤",
        "DELETE": "🗑️",
        "PATCH": "🔧",
        "OPTIONS": "❓",
        "HEAD": "👀"
    }
    return method_emojis.get(method, "📡")


def get_status_color_and_emoji(status_code: int) -> tuple[str, str]:
    if status_code < 200:
        return Fore.BLUE, "ℹ️"
    elif status_code < 300:
        return Fore.GREEN, "✅"
    elif status_code < 400:
        return Fore.YELLOW, "↪️"
    elif status_code < 500:
        return Fore.RED, "⚠️"
    else:
        return Fore.MAGENTA, "❌"


def format_time(seconds: float) -> str:
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f}µs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        method_emoji = get_method_emoji(request.method)

        response = await call_next(request)

        processing_time = time.time() - start_time
        formatted_time = format_time(processing_time)
        status_color, status_emoji = get_status_color_and_emoji(response.status_code)

        # Format the log message
        message = (
            f"{Fore.CYAN}{request.client.host}:{request.client.port}{Style.RESET_ALL} - "
            f"{method_emoji} {Fore.YELLOW}{request.method}{Style.RESET_ALL} - "
            f"{Fore.WHITE}{request.url.path}{Style.RESET_ALL} - "
            f"{status_color}{response.status_code}{Style.RESET_ALL} {status_emoji} - "
            f"⏱️ {Fore.BLUE}{formatted_time}{Style.RESET_ALL}"
        )

        print(message)
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
        ]
    )