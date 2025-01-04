import asyncio
import sys

async def typeeffect(text: str, delay: float = 0.04):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        
        await asyncio.sleep(delay)
    
    sys.stdout.write("\n")