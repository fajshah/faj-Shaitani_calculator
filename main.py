import os
import random
import chainlit as cl
from dotenv import load_dotenv

# Load your Gemini API key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# ===== Function Tools with Evil Twist =====

def add(a: int, b: int) -> int:
    return a + b + random.randint(1, 10)

def sub(a: int, b: int) -> int:
    return a - b - random.randint(1, 10)

def multiply(a: int, b: int) -> int:
    return a * b * random.randint(2, 6)

def divide(a: int, b: int) -> float:
    if b == 0:
        return float('inf')
    return (a / b) + random.uniform(1.0, 5.0)

# ========= Chainlit App Start =========

@cl.on_message
async def main(message: cl.Message):
    try:
        parts = message.content.strip().split()

        if len(parts) != 3:
            await cl.Message(content="❌ Format: `add 2 3`").send()
            return

        op, a, b = parts[0].lower(), int(parts[1]), int(parts[2])

        if op == "add":
            result = add(a, b)
        elif op == "sub":
            result = sub(a, b)
        elif op == "multiply":
            result = multiply(a, b)
        elif op == "divide":
            result = divide(a, b)
        else:
            await cl.Message(content="❌ Unknown operation. Use: add, sub, multiply, divide").send()
            return

        await cl.Message(content=f"😈 Result: {result}").send()

    except Exception as e:
        await cl.Message(content=f"🚨 Error: {e}").send()
