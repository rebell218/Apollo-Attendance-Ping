import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx, message_id: int):
    try:
        message = await ctx.channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.send("Message not found.")
        return
    except discord.errors.DiscordException as e:
        await ctx.send(f"Error fetching message: {e}")
        return
        
# Extract the Users from the Embed of the Apollo Event message (Accepted, Declined, Tentative) and normalize their names. Then sort them into "Non responders" and "Responded users" 
    try:
        responded_users = []
        if message.embeds:
            for embed in message.embeds:
                print(f"Embed: {embed.to_dict()}")
                for field in embed.fields:
                    print(f"Field name: {field.name}")
                    print(f"Field value (raw): {field.value}")

                    if field.name.startswith("<:accepted:") or field.name.startswith("<:declined:") or field.name.startswith("<:tentative:"):
                        responded_users_raw = field.value.splitlines()
                        cleaned_users = [
                            user.strip()[3:].strip().lower() if user.strip().startswith(">>>") else user.strip().lower()
                            for user in responded_users_raw if user.strip()
                        ]
                        print(f"Responded users cleaned (normalized): {cleaned_users}")
                        responded_users.extend(cleaned_users)

        print(f"Responded users (cleaned and normalized): {responded_users}")

    except Exception as e:
        await ctx.send(f"Error processing message content: {e}")
        return
        
        
#Ping all members of group "Non Responders"
    channel_members = ctx.channel.members
    non_responders = []

    for member in channel_members:
        if not member.bot:
            member_name = member.display_name.strip().lower()
            print(f"Checking member: {member.display_name} (normalized: {member_name})")
            if member_name not in responded_users:
                print(f"{member.display_name} has not responded, adding to non_responders.")
                non_responders.append(member)
            else:
                print(f"{member.display_name} has responded.")

    if non_responders:
        non_responder_mentions = " ".join([member.mention for member in non_responders])
        await ctx.send(f"Please respond to the Event {non_responder_mentions}")
    else:
        await ctx.send("All users with access to this channel have responded!")


# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot.run("Your Bot Token HERE")
