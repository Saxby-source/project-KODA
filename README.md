# project-KODA

K.O.D.A. NEXUS v2.1 | System Manual
Designation: Knowledge-Oriented Digital Assistant

Architectural Standard: The Scholar Protocol (SOLID / DRY / Async)

1. System Overview
The K.O.D.A. Nexus is a multi-node, context-aware AI ecosystem. Unlike standard chatbots, it utilizes a "Double-Stack" architecture that combines a permanent global identity with swappable skill modules.

Current Features:
Modular Cognition: Hot-swappable personalities (Scholar, Designer, Alchemist, etc.) via / commands.

Episodic Memory: Persistent SQL-based chat history that survives server restarts.

Direct-Link Networking: USB-Tethering bypass for restricted network environments.

Multi-Device Sync: Real-time broadcasting to any device connected to the local Nexus network.

2. Operational Procedures
Activating the Virtual Environment (The "Venv")
Before running any script, you must isolate the Python environment to ensure library compatibility.

macOS/Linux: source venv/bin/activate

Windows: .\venv\Scripts\activate

Initializing the Nexus (The Server)
To start the "Brain" and begin listening for connections:

Bash

python main.py
The server will default to 0.0.0.0:8000, making it visible to your phone via your Mac's IP address.

Accessing the HMI (The Interface)
Find your Mac's IP (System Settings > Network > Details).

On your phone or desktop browser, navigate to: http://[YOUR_IP]:8000

3. Diagnostic & Maintenance Tools
We use specialized diagnostic scripts to ensure the "Neural Pathways" are clear.

check_brain.py
Purpose: Queries the Google Gemini API to list exactly which models are authorized for your specific API key.

Why use it? In 2026, model names (e.g., gemini-2.0-flash) and API endpoints (v1 vs v1beta) change frequently. This script removes the guesswork by showing you exactly what "brains" are available to plug into main.py.

koda_vault.db
Purpose: A SQLite database holding the history and lessons tables.

Maintenance: This file is created automatically. If you ever wish to "wipe" K.O.D.A.'s memory entirely, simply delete this file.

4. Logical Architecture (For the Scholar)
The Switchboard: Located in main.py, it intercepts any input starting with /. This allows for zero-latency reconfiguration of the AI's internal rules without a reboot.

Strict Schema Validation: We utilize google.genai.types (Content, Part) to ensure the JSON payloads sent to Google match the 2026 Pydantic requirements. This prevents the "Validation Errors" common in legacy code.

State Persistence: By using get_recent_history(limit=10), we feed the last 5 turns of conversation (User + Model) back into the prompt. This provides the AI with "Object Permanence."

5. Tomorrow's Objective: Synaptic Refinement
Our next session will focus on the lessons table.

The Goal: Moving beyond simple "Chat History" into "Learned Rules."

The Logic: We will build a function that allows K.O.D.A. to extract specific user preferences (e.g., "Always use tabs, not spaces") and store them as permanent "Synapses" that take priority over the base module instructions.