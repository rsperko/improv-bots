from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scene.scene_manager import SceneManager
import os
from dotenv import load_dotenv
from config import setup_logging

load_dotenv()

setup_logging(os.getenv("ENVIRONMENT", "dev"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scene_manager = SceneManager()

class Suggestion(BaseModel):
    text: str

@app.post("/start_scene")
async def start_scene(suggestion: Suggestion):
    return scene_manager.start_scene(suggestion.text)

@app.get("/next_turn")
async def next_turn():
    return scene_manager.next_turn()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
