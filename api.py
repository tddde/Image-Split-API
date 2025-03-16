import os
import subprocess
import sys

def install_dependencies():
    required_packages = ["fastapi", "uvicorn", "pillow"]
    for package in required_packages:
        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

install_dependencies()

from fastapi import FastAPI
from fastapi.responses import FileResponse
from PIL import Image

app = FastAPI()

def create_image(colour: str, width: int, height: int, filename: str):
    colour = tuple(int(colour[i:i+2], 16) for i in (0, 2, 4))
    img = Image.new("RGB", (width, height), colour)
    img.save(filename)

@app.get("/image-split")
async def generate_image(colour: str = "00e3b0", width: int = 300, height: int = 3):
    filename = "output.png"
    create_image(colour, width, height, filename)
    return FileResponse(filename, media_type="image/png")

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 25568))
    uvicorn.run(app, host="0.0.0.0", port=port)
