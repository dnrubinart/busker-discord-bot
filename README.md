<h1 align="center"><img src="https://i.imgur.com/06ZNSjG.png" width="128"><br/>Omnia</h1>

**Omnia** is a discord bot designed to be a multipurpose bot with a variety of features focused on bringing your server to life. The bot is currently in development and is not yet ready for public use.

## Table of Contents

- [Features](#features)
- [Commands](#commands)
    - [Music commands](#music-commands)
    - [Moderation commands](#moderation-commands)
    - [Generation commands](#generation-commands)
    - [Information commands](#information-commands)
- [Quick start](#quick-start)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)

## Features

- Variety of commands with embeds and aliases.
- Music player with support for YouTube.
- Commands to simplify server management.
- Generation of images with prompts.
- Support for LLM models, currently uses Ollama3. Allows for detailed assistance directly in your server.
- Detailed information about the commands and how to use them.

## Commands

### Music commands:
- `!play <song>` - Plays a song by providing a search query or a link.
- `!pause` - Pauses the current song.
- `!resume` - Resumes the current song.
- `!skip` - Skips the current song.
- `!queue` - Displays the current queue.
- `!clear` - Clears the queue.
- `!disconnect` - Disconnects the bot from the voice channel.

### Moderation commands:
- `!kick <member> <reason>` - Kicks a member from the server. Providing a reason is optional.
- `!ban <member> <reason>` - Bans a member from the server. Providing a reason is optional.
- `!unban <member>` - Unbans a member from the server.
- `!timeout <member> <time>` - Times out a member for a specified amount of time.
- `!rmtimeout <member>` - Removes the timeout from a member.

### Generation commands:
- `!draw <prompt>` - Generates an image based on the provided prompt. Uses Stable Diffusion 3 API to generate images.
- `!ask <prompt>` - Generates a response based on the provided prompt. Uses Ollama3 API to generate responses.

### Information commands:
- `!help` - Displays a list of all commands except moderation commands and how to use them.
- `!ahelp` - Displays a list of all moderation commands and how to use them if you have the required permissions.

## Quick start

### Prerequisites:

- Python 3.10 or higher
- Discord Application in the [Discord Developer Portal](https://discord.com/developers/applications)
- [Ollama](https://ollama.ai/) installed on your local machine
- API key for [Stable Diffusion 3](https://platform.stability.ai/account/keys)

### Installation:

1. Clone the repository.
2. Install the required dependencies ```pip install -r requirements.txt```
3. Set up your application in the [Discord Developer Portal](https://discord.com/developers/applications).
4. Create a `.env` file in the root directory of the project by copying the contents of the `.env.example` file.
5. Fill in the required fields in the `.env` file:
- `DISCORD_TOKEN` - Your Discord bot token.
- `STABILITY_API_KEY` - Your API key for Stable Diffusion 3.
- `OLLAMA_HOST` - The host of your Ollama instance.
- `OLLAMA_MODEL` - The model name used by your Ollama instance.
6. Install Ollama on your local machine. Instructions can be found [here](https://github.com/ollama/ollama).
7. Run the bot.