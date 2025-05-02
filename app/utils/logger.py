import os

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

def log_info(message: str):
    if DEBUG:
        print(f"[INFO] {message}")

def log_error(message: str):
    if DEBUG:
        print(f"[ERROR] {message}")
