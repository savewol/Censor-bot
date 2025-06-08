import discord
from discord.ext import commands

# --- SETUP INTENTS ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# --- BOT SETUP ---
bot = commands.Bot(command_prefix="!", intents=intents)

# --- BANNED WORD LIST ---
banned_words = ["nigger", "dox", "fag", "faggot", "cunt"]  # lowercase for detection

@bot.event
async def on_ready():
    print(f"✅ Bot is ready. Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    msg_content = message.content.lower()
    triggered = any(word in msg_content for word in banned_words)

    if triggered:
        guild_me = message.guild.me
        perms = message.channel.permissions_for(guild_me)

        if perms.manage_messages and guild_me.top_role > message.author.top_role:
            try:
                await message.delete()
            except discord.Forbidden:
                print("❌ Missing permission to delete message.")
        else:
            print("⚠️ Can't delete message due to missing permission or role hierarchy.")

        if perms.send_messages:
            embed = discord.Embed(
                description=(
                    "**You're not allowed to say that.**\n\n"
                    "List Of Words That Are Censored:\n"
                    "- Hard R\n"
                    "- D*x\n"
                    "- Fed\n"
                    "- F Slur\n\n"
                    "If you believe this was a mistake, please report to <@790338202103316531>"
                ),
                color=discord.Color.red()
            )

            if perms.embed_links:
                try:
                    await message.channel.send(embed=embed)
                except Exception as e:
                    print(f"❌ Failed to send embed: {e}")
            else:
                try:
                    await message.channel.send(embed.description)
                except Exception as e:
                    print(f"❌ Failed to send fallback warning: {e}")
        else:
            print("❌ Can't send warning: missing Send Messages permission.")

        return

    await bot.process_commands(message)

# --- RUN BOT ---
bot.run("MTM4MTExMTM3Mzk3NDYwNTkzNQ.GhM-bT.I2E4nRORBns0jTdkOjxuEJKHdj58Yuni3a_i9w")  # Replace with your actual bot token
