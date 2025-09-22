import os
import discord

TOKEN = os.getenv("DISCORD_TOKEN")
LIMITED_CHANNEL_ID = int(os.getenv("LIMITED_CHANNEL_ID", "0"))
MAX_WORDS = int(os.getenv("MAX_WORDS", "50"))
# Optional: comma-separated role IDs that can bypass the limit
EXEMPT_ROLE_IDS = {int(r) for r in os.getenv("EXEMPT_ROLE_IDS", "").split(",") if r.strip()}

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.id != LIMITED_CHANNEL_ID:
        return

    # Optional exemptions by role
    if EXEMPT_ROLE_IDS and isinstance(message.author, discord.Member):
        if any(role.id in EXEMPT_ROLE_IDS for role in message.author.roles):
            return

    word_count = len(message.content.split())
    if word_count > MAX_WORDS:
        try:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} your message had **{word_count}** words. "
                f"Limit is **{MAX_WORDS}**. Please shorten it.",
                delete_after=6
            )
        except discord.Forbidden:
            await message.channel.send(
                "I need **Manage Messages** permission in this channel to enforce the word limit.",
                delete_after=8
            )

if __name__ == "__main__":
    client.run(TOKEN)
