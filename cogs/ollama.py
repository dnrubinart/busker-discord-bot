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
        """Generates a response based on the prompt using the Ollama API."""
        async with aiohttp.ClientSession() as session:
            request_data = {"model": self.model, "prompt": prompt}
            async with session.post(
                f"{self.base_url}/api/generate", json=request_data
            ) as response:
                if response.status == 200:
                    full_response = await response.text()
                    return self.parse_response(full_response)
                else:
                    error = await response.text()
                    return f"Error: {response.status} - {error}"

    def parse_response(self, response_text):
        """Parses the response from the Ollama API.
        The response is in the format of a JSON object per line.
        This function extracts the "response" field from each JSON object."""
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
        """Asks Ollama a question and generates a response."""
        await ctx.send("Processing your request...")
        response = await self.generate(prompt)

        full_response = f"**Question:** {prompt}\n\n**Answer:** {response}"
        response_segments = [
            full_response[i : i + 1900] for i in range(0, len(full_response), 1900)
        ]

        await ctx.send(response_segments[0])
        for segment in response_segments[1:]:
            await ctx.send(segment)
