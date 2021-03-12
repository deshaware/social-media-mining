import twitter, json

WORLD_WOE_ID = 1
US_WOE_ID = 23424977
# SYRACUSE_WOE_ID = 2503418

SYRACUSE_WOE_ID = 3369 #OTTAWA

CONSUMER_KEY = 'bblGvcSnJgCpykQ9PIs8Y4BL2'
CONSUMER_SECRET = 'lggBEFHvgHOVUqMBiPlqVyDqFSpPJwwAGFl0VcNlcSlwsn5cON'
OAUTH_TOKEN = '141631266-M6Q8T7sdfHCEBIS02itrNTuoQAD6CTHENFFVPb4m'
OAUTH_TOKEN_SECRET = '7gbh3rQXGDciJT8MwhIeB3azQjWbJgZGIq28J17MgvJan'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
# us_trends = twitter_api.trends.place(_id=US_WOE_ID)
# print(json.dumps(us_trends,indent=1))

# f = open('us_trends.txt', 'w')
# print(json.dumps(us_trends))

# print(world_trends)
# print()
# print(us_trends)

# my_trend = twitter_api.trends.place(_id=SYRACUSE_WOE_ID)
# print(json.dumps(my_trend, indent=1))


# trends_closest= twitter_api.trends.closest(lat=43.048122, long=-76.147423)
# print(json.dumps(trends_closest,indent=1))

q = 'Arsenal'
count = 10
search_results = twitter_api.search.tweets(q=q, count=count)
print(json.dumps(search_results, indent=1, sort_keys=True))

# print(search_results)
