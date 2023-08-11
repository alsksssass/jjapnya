import discord
from collections import Counter

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        # Get a list of all user IDs in the guild, excluding the guild owner's ID
        user_ids = [member.id for member in guild.members if member.id != guild.owner_id]
        
        # Count the occurrences of each user ID
        user_counts = Counter(user_ids)
        
        # Get the top 3 most common user IDs
        top_3 = user_counts.most_common(3)
        
        # Check for ties and include them in the top 3
        tied_users = [user for user, count in user_counts.items() if count == top_3[-1][1] and user not in [x[0] for x in top_3]]
        top_3.extend([(user, top_3[-1][1]) for user in tied_users])
        
        # Print the results
        print(f"Top 3 users (excluding guild owner) in guild {guild.name}:")
        for i, (user_id, count) in enumerate(top_3):
            print(f"{i+1}. User ID: {user_id}, Count: {count}")

client.run("YOUR_BOT_TOKEN_HERE")
