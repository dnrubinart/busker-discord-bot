import json
import os

import aiohttp
from discord.ext import commands


class Ollama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = os.getenv("OLLAMA_HOST")
        self.model = os.getenv("OLLAMA_MODEL")

    async def generate(self, prompt):
        async with aiohttp.ClientSession() as session:
            request_data = {"model": self.model, "prompt": prompt}
            async with session.post(
                f"{self.base_url}/api/generate", json=request_data
            ) as response:
                if response.status == 200:
                    full_response = await response.text()
                    return self.parse_response(full_response)
                else:
                    error_text = await response.text()
                    return f"Error: {response.status} - {error_text}"

    def parse_response(self, response_text):
        lines = response_text.strip().split("\n")
        parsed_response = ""
        for line in lines:
            try:
                data = json.loads(line)
                if "response" in data:
                    parsed_response += data["response"]
            except json.JSONDecodeError:
                continue
        return parsed_response.strip()

    @commands.command(name="ask")
    async def ask(self, ctx, *, prompt: str):
        await ctx.send("Processing your request...")
        response = await self.generate(prompt)

        full_response = f"prompt: {prompt}\n\nAnswer: {response}"
        response_segments = [
            full_response[i : i + 1900] for i in range(0, len(full_response), 1900)
        ]

        await ctx.send(response_segments[0])
        for chunk in response_segments[1:]:
            await ctx.send(chunk)
