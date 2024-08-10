import io
import os

import discord
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from discord.ext import commands
from PIL import Image
from stability_sdk import client


class Art(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stability = client.StabilityInference(
            key=os.environ["STABILITY_API_KEY"],
            verbose=True,
        )

    @commands.command(name="generate", aliases=["gen"])
    async def generate(self, ctx, *, prompt):
        """Generates an image based on the prompt."""
        message = await ctx.send("Generating...")
        generated_responses = self.stability.generate(prompt=prompt.strip())

        for response in generated_responses:
            for artifact in response.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    await ctx.send(
                        "Could not process the request due to safety filters."
                    )
                elif artifact.type == generation.ARTIFACT_IMAGE:
                    image = Image.open(io.BytesIO(artifact.binary))
                    image_stream = io.BytesIO(artifact.binary)
                    image.save(image_stream, format="PNG")
                    image_stream.seek(0)
                    image_file = discord.File(image_stream, filename="image.png")
                    await message.edit(content=f"“{prompt}” \n")
                    await ctx.send(file=image_file)
