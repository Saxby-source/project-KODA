"""
K.O.D.A. NEXUS v2.1
Architect: The Scholar
Project: Knowledge-Oriented Digital Assistant
"""

import os
import logging
from typing import List
from pydantic import BaseModel

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from google import genai
from google.genai import types, errors
from dotenv import load_dotenv

from memory_core import init_db, save_message, get_recent_history

# --- Configuration ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Nexus")

app = FastAPI(title="K.O.D.A. Nexus")

class NexusState(BaseModel):
    """Encapsulates system state to ensure single source of truth."""
    active_module: str = "scholar"
    model_id: str = "gemini-2.0-flash"

state = NexusState()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), http_options=types.HttpOptions(api_version="v1beta"))

# --- Logic Layer ---

def get_system_prompt() -> str:
    """Compiles the operational persona for the current session."""
    def read_mod(m):
        try:
            with open(f"modules/{m}.txt", "r") as f: return f.read()
        except FileNotFoundError: return ""
    
    return f"{read_mod('main_identity')}\n\n[PROTOCOL: {state.active_module}]\n{read_mod(state.active_module)}"

# --- Networking ---

class ConnectionManager:
    """Manages multi-node WebSocket lifecycle."""
    def __init__(self):
        self.nodes: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.nodes.append(ws)

    def disconnect(self, ws: WebSocket):
        self.nodes.remove(ws)

    async def broadcast(self, message: str):
        for node in self.nodes:
            await node.send_text(message)

nexus_manager = ConnectionManager()

# --- Endpoints ---
@app.get("/")
async def serve_interface():
    """
    Serves the HMI. 
    Uses absolute pathing to prevent 404s in different environments.
    """
    # Get the directory where main.py actually lives
    base_path = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_path, "index.html")
    
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        logger.error(f"CRITICAL: index.html not found at {html_path}")
        return HTMLResponse("<h2>System Error: HMI Source Missing</h2>", status_code=404)

@app.websocket("/ws/{client_id}")
async def nexus_bridge(websocket: WebSocket, client_id: str):
    await nexus_manager.connect(websocket)
    init_db() # Ensure DB readiness
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Switchboard check
            if data.startswith("/"):
                await handle_switchboard(data)
                continue

            # Synthesis
            history = get_recent_history(limit=10)
            save_message("user", data)

            try:
                system_prompt = get_system_prompt()
                
                # Create the 'Current Message' object
                current_message = types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=data)]
                )

                response = client.models.generate_content(
                    model=state.model_id,
                    # Join the history list with the current message object
                    contents=history + [current_message], 
                    config=types.GenerateContentConfig(
                        system_instruction=[types.Part.from_text(text=system_prompt)],
                        temperature=0.2
                    )
                )
                
                reply = response.text
                save_message("model", reply)
                await nexus_manager.broadcast(reply)

            except errors.ClientError as e:
                await nexus_manager.broadcast(f"⚠️ INTERNAL_FAULT: {e}")

    except WebSocketDisconnect:
        nexus_manager.disconnect(websocket)

async def handle_switchboard(cmd: str):
    """Processes hot-swapping of cognitive modules."""
    module = cmd[1:].lower()
    if module in ["scholar", "designer", "partner", "alchemist", "fixer", "influencer"]:
        state.active_module = module
        await nexus_manager.broadcast(f"🔄 SYSTEM_SYNC: Module [{module.upper()}] online.")
    else:
        await nexus_manager.broadcast(f"❌ ERROR: Module [{module}] unknown.")