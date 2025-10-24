# Instagnite

Define an AI-powered agent and advertise your product while you sleep.

## How it works?
The bot listens for notifications using the MQTT protocol. When it receives a new message, it adds it to the queue 
system, where it holds conversations in real time, based on the instructions you give it.

A lookout at the program and an example of the bot's chat style:

![showcase](showcase.png)

> [!IMPORTANT]
> Instagnite is in a pre-alpha state, and only suitable for use by developers. The bot uses third-party scripts 
> that may violate Instagram's terms of use. You use it your own risk.
>

## Basic requirements
- Node.js >= 18 (for JS deps like instagram-private-api and instagram_mqtt)
- Python >= 3.11 (for backend and xAI integration)
- uv (https://docs.astral.sh/uv/) – Python package manager
- xAI API key – for the SDK

### Python deps 
fastapi, instagrapi, pydantic-settings, pyotp, pytest, python-dotenv, typer, uvicorn[standard], xai-sdk (all >= latest stable)

### Node.js deps
instagram-private-api, instagram_mqtt



## Config

1. In the virtual environment created with the requirements as above, clone the repository:
```
git clone https://github.com/uvavn/instagnite.git
cd instagnite
```
2. Install dependencies:
```
npm ci
uv sync
```

3. Copy .env and credentials.json, then **fill the variables manually with your data**:
```
cp "example .env" .env
cp "example credentials.json" credentials.json
```

## AI Instructions
The entire personality of the bot should be defined in the 
[ai_instructions/basic.txt](https://github.com/uvavn/instagnite/blob/master/ai_instructions/basic.txt) file. 
It is there that you give precise instructions as to how to redirect the conversation. Be specific and detailed. In the file there is already a simple example of how it can look like - customize it under you.

In the 
[ai_instructions/stop_responding.txt](https://github.com/uvavn/instagnite/blob/master/ai_instructions/stop_responding.txt) 
file, you can define when you want the bot to end conversations and not respond to future user messages.

## Usage

When you have everything prepared run the script (requires host="127.0.0.1", port=8000 available) by 
typing the command:
```
ignite chatbot
```
From now on, the bot will listen and respond to messages until you decide to disable the program.


## Contact
If you have any questions - feel free to contact me [here](https://t.me/synthavn). 
Also, in case you want to help with develop or test the project I can provide xAI key.












