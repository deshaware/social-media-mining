import twitter, json

CONSUMER_KEY = 'bblGvcSnJgCpykQ9PIs8Y4BL2'
CONSUMER_SECRET = 'lggBEFHvgHOVUqMBiPlqVyDqFSpPJwwAGFl0VcNlcSlwsn5cON'
OAUTH_TOKEN = '141631266-M6Q8T7sdfHCEBIS02itrNTuoQAD6CTHENFFVPb4m'
OAUTH_TOKEN_SECRET = '7gbh3rQXGDciJT8MwhIeB3azQjWbJgZGIq28J17MgvJan'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# user = twitter_api.users.show(screen_name='katyperry')
# user = twitter_api.users.show(user_id=21447363)

# print(json.dumps(user,indent=1,sort_keys=True))

# user_search = twitter_api.users.search(q='Deshaware')
# print(json.dumps(user_search,indent=1,sort_keys=True))



# User show only 1 profile
# User Lookup gives a lots of profile

# Always use lookup, not show
# user_lookup = twitter_api.users.lookup(user_id='813286,27260086')
# print(json.dumps(user_lookup,indent=1,sort_keys=True))

# for i in user_lookup:
#     print(i['screen_name'])


followers = twitter_api.friends.ids(screen_name='Swapnil Deshaware',count=30, cursor=1676124742528216900)
print(json.dumps(followers,indent=1,sort_keys=True))

# id = '1309238390261534721,748410918174875649,726953658856931328,2424767945,140923963,1305543196500537346,245321457,949962577777430528,129809688,82060183,1288323498964922368,1116860554902233088,2915308411,1267389780754608130,937701413555134464,2918216216,3146644511,971445617938624515,974764801242132482,351100725,819617030278180864,810156246602956801,3069356473,867841359020937217,2748898717,23829268,3256337594,82917803,2288518088,118740608'
id = '468741166,318571154,478227449,716119409786535936,2426422297,91985735,1566463268,70345946,60986611,330262748,571964518,850747214909423616,1297009600248664065,389681470,1069636036291112960,1037163655895207936,813333008,491821358,1704118916,341643950,1668100142,1219219876637827073,107768032,870038005,2330223926,2600210567,1057398307935473669,351109380,82060183,272839561'
user_lookup = twitter_api.users.lookup(user_id=id)
# print(json.dumps(user_lookup,indent=1,sort_keys=True))

for i in user_lookup:
    print(i['screen_name'])