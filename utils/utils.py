import json

async def read_user():
    with open("user.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Extract the list of usernames
    user_list = [user["username"] for user in data]

    return user_list

async def export_txt(formatted_tweets):
    with open("output_tweets.txt", "a", encoding="utf-8") as f:
        f.write("\n\n\n")
        f.write(formatted_tweets)
    print("✅ Tweets exported to output_tweets.txt")