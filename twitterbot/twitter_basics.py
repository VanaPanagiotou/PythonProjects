import tweepy
import config  # config.py : where I keep my keys as constants

client = tweepy.Client(
    bearer_token=config.BEARER_TOKEN,
    consumer_key=config.API_KEY,
    consumer_secret=config.API_SECRET,
    access_token=config.ACCESS_TOKEN,
    access_token_secret=config.ACCESS_TOKEN_SECRET,
)


print("Basic information about my Twitter account:\n")

me = client.get_me(user_fields=["created_at", "description", "location", "profile_image_url", "public_metrics"])
print(f"My name: {me.data.name}")
print(f"My handle: @{me.data.username}")
print(f"My Id: {me.data.id}")
print(f"Date that my Twitter account was created: {me.data.created_at}")
print(f"My bio: {me.data.description}")
print(f"My location: {me.data.location}")
print(f"My Profile pic: {me.data.profile_image_url}")
print(f"My followers count: {me.data.public_metrics['followers_count']}")
print(f"My following count: {me.data.public_metrics['following_count']}")
print('')

###########################################################################################################

print("My Home Timeline:\n")

user_timeline = client.get_home_timeline()
for tweet in user_timeline.data:
    print(tweet.text)
    # print(tweet.id)
print('')

###########################################################################################################

print("Print a User's latest Tweets:\n")

# Define a Twitter account for investigation
user_account = client.get_user(username="zerotomasteryio")

public_tweets = client.get_users_tweets(user_account.data.id)
for tweet in public_tweets.data:
    print(tweet.text)
print('')

###########################################################################################################

print("Print a User's Followers:\n")

user_followers = client.get_users_followers(user_account.data.id, user_fields=['public_metrics'])
for follower in user_followers.data:
    print(f"{follower.name} with {follower.public_metrics['followers_count']} followers and {follower.public_metrics['following_count']} following")
print('')

###########################################################################################################

print("Print Users that a User Follows:\n")

user_following = client.get_users_following(user_account.data.id, user_fields=['public_metrics'])
for following in user_following.data:
    print(f"{following.name} with {following.public_metrics['followers_count']} followers and {following.public_metrics['following_count']} following")
print('')

###########################################################################################################

print("Print a User's mentions:\n")

user_mentions = client.get_users_mentions(user_account.data.id, tweet_fields=['conversation_id', 'created_at'])
for tweet in user_mentions.data:
    print(f"Tweet: {tweet.text}\nThe original Tweet ID of the conversation is {tweet.conversation_id} and was created on {tweet.created_at}.\n")
print('')

###########################################################################################################

print("Print Users that like a specific Tweet:\n")

# Define a Twitter id for investigation
tweet_id = 1532061046688534528

users_like_tweet = client.get_liking_users(tweet_id, user_fields=['public_metrics'])
for user in users_like_tweet.data:
    print(f"{user.name} with {user.public_metrics['followers_count']} followers and {user.public_metrics['following_count']} following")
print('')

###########################################################################################################

print("Print Users that retweeted a specific Tweet:\n")

users_retweeted_tweet = client.get_retweeters(tweet_id, user_fields=['public_metrics'])
for user in users_retweeted_tweet.data:
    print(f"{user.name} with {user.public_metrics['followers_count']} followers and {user.public_metrics['following_count']} following")
print('')

##########################################################################################################

print("Print Tweets that a user a liked:\n")

tweets_user_liked = client.get_liked_tweets(user_account.data.id, tweet_fields=['conversation_id', 'created_at'])
for tweet in tweets_user_liked.data:
    print(f"Tweet: {tweet.text}\nThe original Tweet ID of the conversation is {tweet.conversation_id} and was created on {tweet.created_at}.\n")
print('')

##########################################################################################################

print("Print Tweets that a user liked:\n")

tweets_user_liked = client.get_liked_tweets(user_account.data.id, tweet_fields=['conversation_id', 'created_at'])
for tweet in tweets_user_liked.data:
    print(f"Tweet: {tweet.text}\nThe original Tweet ID of the conversation is {tweet.conversation_id} and was created on {tweet.created_at}.\n")
print('')

##########################################################################################################

print("Print Tweets with user information:\n")

# Define a search query
query = 'happy OR #love'  # containing either “happy” or “#love” (or both)
tweets = client.search_recent_tweets(query=query, tweet_fields=['created_at'],
                                     user_fields=['public_metrics', 'profile_image_url'], expansions='author_id',
                                     max_results=100)

# Get users list from the includes object
users = {u["id"]: u for u in tweets.includes['users']}

for tweet in tweets.data:
    if users[tweet.author_id]:
        user = users[tweet.author_id]
        print(f"Tweet: {tweet.text}\nUser details: {user.name} with {user.public_metrics['followers_count']} followers and {user.public_metrics['following_count']} following and profile image URL: {user.profile_image_url}\n")
print('')

##########################################################################################################

print("Print Tweets with media information:\n")

# Define a search query
query = '(happy OR #love) has:media'  # contain either “happy” or “#love” (or both) and a media object, such as a photo, GIF, or video
tweets = client.search_recent_tweets(query=query, tweet_fields=['attachments', 'created_at'],
                                     media_fields=['preview_image_url'],
                                     expansions='attachments.media_keys', max_results=100)

# Get list of media from the includes object
media = {m["media_key"]: m for m in tweets.includes['media']}
for tweet in tweets.data:
    if 'attachments' in tweet.data:
        attachments = tweet.data['attachments']
        media_keys = attachments['media_keys']
        print(f"Tweet: {tweet.text}\n")
        if media[media_keys[0]].preview_image_url:
            print(media[media_keys[0]].preview_image_url)
print('')

##########################################################################################################

print("Print Tweets count for a defined search query:\n")

# Define a search query
query = '(happy OR #love)'  # contain either “happy” or “#love” (or both) and a media object, such as a photo, GIF, or video
counts = client.get_recent_tweets_count(query=query, granularity='day')

for count in counts.data:
    print(f"From {count['start']} to {count['end']}: {count['tweet_count']} times")
print('')

#########################################################################################################

print("Print Tweets from a defined User from the last 7 days:\n")

# Define a search query
query = 'from:zerotomasteryio -is:retweet'  # tweets from a specific user, excluding retweets

tweets = client.search_recent_tweets(query=query, tweet_fields=['conversation_id', 'created_at'],
                                     max_results=100)

for tweet in tweets.data:
    print(
        f"Tweet: {tweet.text}\nThe original Tweet ID of the conversation is {tweet.conversation_id} and was created on {tweet.created_at}.\n")
print('')

#########################################################################################################

print("Getting more than 100 tweets at a time:\n")

# Define a search query
query = 'happy OR #love'  # contain either “happy” or “#love” (or both)

# limit: maximum number of Tweets you want to get
for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields=['conversation_id', 'created_at'], max_results=100).flatten(limit=200):
    print(
        f"Tweet: {tweet.text}\nThe original Tweet ID of the conversation is {tweet.conversation_id} and was created on {tweet.created_at}.\n")
print('')

#########################################################################################################

print("Searching for Tweets using Tweet IDs:\n")

tweet_ids = ['1533813165007699969', '1533807724470976514', '1533813168899870720']
tweets = client.get_tweets(ids=tweet_ids, tweet_fields=['created_at'])

for tweet in tweets.data:
    print(f"Tweet: {tweet.text}\nCreated Date: {tweet.created_at}\n")
print('')

#########################################################################################################

print("Searching for Users using User IDs:\n")

user_ids = ['167223139', '354351428', '3050535434']
users = client.get_users(ids=user_ids, user_fields=['public_metrics', 'profile_image_url'])

for user in users.data:
    print(
        f"User details: {user.name} with {user.public_metrics['followers_count']} followers and {user.public_metrics['following_count']} following and profile image URL: {user.profile_image_url}\n")
print('')

#########################################################################################################

print("Create and post a Tweet!\n")
response = client.create_tweet(text='Hello world! My first tweet! :)')  # text: whatever you want to Tweet about
print('')

#########################################################################################################

print("Retweet a Tweet!\n")
response = client.retweet(1532061046688534528)  # Tweet ID that you want to retweet
print('')

#########################################################################################################

print("Reply to a Tweet!\n")
response = client.create_tweet(text='Hello world reply!',
                               in_reply_to_tweet_id=1533824832974082049)  # text: whatever you want to Tweet about
print('')

#########################################################################################################

print("Like Tweets that contain a defined search query!\n")

# Define a search query
query = '"Python language"'  # match the exact phrase

tweets = client.search_recent_tweets(query=query, tweet_fields=['public_metrics'],
                                     max_results=10)
for tweet in tweets.data:
    client.like(tweet.id)  # Tweet ID that you want to like
    print(f"Liking tweet {tweet.id}!")

