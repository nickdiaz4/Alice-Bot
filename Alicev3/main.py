import os

import discord
from discord import app_commands
from huggingface_hub import InferenceClient


class MyClient(discord.Client):

    # initialzie the hugging face inference model
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.alice_client = InferenceClient(
            "walletfullofones/DialoGPT-small-Alice",
            token=os.environ["HUGGINGFACE_TOKEN"],
        )

    async def on_ready(self):
        if self.user:
            print(f'{self.user.name} IS ONLINE')
            print(self.user.id)
        print('------')
        await self.register_commands()
        await self.tree.sync()
        await self.query("wake up")

    # Query the model
    async def query(self, user_message):
        response = ""

        for message in self.alice_client.chat_completion(
                messages=[{
                    "role": "user",
                    "content": user_message
                }],
                max_tokens=500,
                stream=True,
        ):
            # Check if the content is not None before concatenating
            content = message.choices[0].delta.content
            if content is not None:
                response += content

        return response

    async def register_commands(self):

        @app_commands.command(name="alice", description="Chat with Alice!")
        async def alice_command(interaction: discord.Interaction,
                                message: str):
            await interaction.response.defer()
            response = await self.query(message)

            if not response:
                response = "I'm not sure what to say other than I sure do love Isaac lol"

            await interaction.followup.send(response)

        # Register the command to the tree
        self.tree.add_command(alice_command)


def main():
    # Check if DISCORD_TOKEN is in the environment
    client = MyClient()
    if 'DISCORD_TOKEN' in os.environ:
        print("DISCORD_TOKEN found in environment.")
        print(f"Token: {os.environ['DISCORD_TOKEN'][:5]}..."
              )  # Print part of the token for verification
    else:
        print("DISCORD_TOKEN not found in environment.")
        return
    client.run(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':
    main()
