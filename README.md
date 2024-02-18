# SpeechScaffold
SpeechScaffold is a tool which developers run alongside the IDE. The tool allows a developer to rapidly build and iterate on the style and functionality of their React components simply by describing the changes they want out loud. It integrates directly with the IDE, so the developer can instantly edit and use code they generate.

## Installation
You'll need to run Ollama (for local LLM; I used codellama) and you'll need to download a whisper model to /assistant/whisper (I used medium.en.pt). Then, simply run the Ollama server (should be automatic), the assistant (with python3 assistant.py in the folder /assistant), and the client (with npm run dev in the folder /autowebsite).