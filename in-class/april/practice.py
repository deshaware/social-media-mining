import twitter, json
import sys

def twitter_search(twitter_api, q, max_results=200, **kw):


    # See https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    # and https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
    # for details on advanced search criteria that may be useful for 
    # keyword arguments
    
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets    
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    
    statuses = search_results['statuses']
    
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://developer.twitter.com/en/docs/basics/rate-limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    
    # Enforce a reasonable limit
    max_results = min(1000, max_results)
    
    for _ in range(10): # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError as e: # No more results when next_results doesn't exist
            break
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') 
                        for kv in next_results[1:].split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        
        if len(statuses) > max_results: 
            break
            
    return statuses

SYRACUSE_WOE_ID = 3369 #OTTAWA

CONSUMER_KEY = 'bblGvcSnJgCpykQ9PIs8Y4BL2'
CONSUMER_SECRET = 'lggBEFHvgHOVUqMBiPlqVyDqFSpPJwwAGFl0VcNlcSlwsn5cON'
OAUTH_TOKEN = '141631266-M6Q8T7sdfHCEBIS02itrNTuoQAD6CTHENFFVPb4m'
OAUTH_TOKEN_SECRET = '7gbh3rQXGDciJT8MwhIeB3azQjWbJgZGIq28J17MgvJan'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                        CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)
q = "CrossFit"
# results = twitter_search(twitter_api, q, max_results=10)


q = 'CrossFit' # Comma-separated list of terms

print('Filtering the public timeline for track={0}'.format(q), file=sys.stderr)
sys.stderr.flush()

# Returns an instance of twitter.Twitter
# twitter_api = oauth_login()

# Reference the self.auth parameter
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

# See https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data
stream = twitter_stream.statuses.filter(track=q)

# print(json.dumps(results[0], indent=1))

print(json.dumps(stream,indent=1))