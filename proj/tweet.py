import twitter, datetime
import json
import pymongo

# mongo="mongodb+srv://praful:cs18p2IX3N3oSwn2@cluster0.8dzwo.azure.mongodb.net/smdm?retryWrites=true&w=majority"
mongo="mongodb://localhost:27017/"
db = "smdm"

def oauth_login():
    '''
    A static method to authenticate user
    It uses OAuth2.0 specification which takes a bearer token to authenticate user
    '''

    CONSUMER_KEY = 'agQmGHFcg9CDeoUSXUFvdPl lT'
    CONSUMER_SECRET = 'N9rqHRmzCJt4SALlxWOCbYyXno0khHnbFTwBFVnrqEKWA1VlfL'
    BEARER_TOKEN= "AAAAAAAAAAAAAAAAAAAAAE04NwEAAAAAjQ9nJ%2BLef%2Fkj3cM1txJPOBATLJk%3DisQRS6PBXd5VLdOFUFgirQpkoK5oygGUbLMku7G0vYetzIyYJt"
    
    auth = twitter.OAuth2(CONSUMER_KEY, CONSUMER_SECRET, BEARER_TOKEN)
    api = twitter.Twitter(auth=auth)
    return api

def make_twitter_request(api_func, max_errors=10, *args, **kw): 
    '''
    A nested helper function that handles common HTTPErrors. Return an updated
    value for wait_period if the problem is a 500 level error. Block until the
    rate limit is reset if it's a rate limiting issue (429 error). Returns None
    for 401 and 404 errors, which requires special handling by the caller.
    '''

    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
        '''
        This helper function handles run-time error such as 429, it sleeps until the timeout
        This method is referred from Twitter Cookbook
        '''
    
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e    
        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429: 
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again.', file=sys.stderr)
                return 2
            else:
                raise e 
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'.format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise

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

def clean_results(result, topic):
    final = []
    for arr in result["statuses"]:
        obj = dict()
        obj["tweet"] = arr["text"]
        obj["id"] = arr["id_str"]
        obj["name"] = arr["user"]["name"]
        obj["location"] = arr["user"]["location"]
        obj["topic"] = topic
        obj["created_at"] = arr["created_at"]
        obj["processed_on"] = datetime.datetime.now().isoformat(' ', 'seconds')
        final.append(obj)
    return final


def save_tweets(tweets):
    client = pymongo.MongoClient(mongo)
    database = client[db]
    coll = database["smdm"]
    try:
        result = coll.insert_many(tweets)
        print("done inserting")
        return result
    except Exception as e:
        print(e)

def query_tweet(query, count, topic, dates):
    api = oauth_login()
    for i in range(0,len(dates) - 2):
        # fromDate = (datetime.date.strptime(toDate, '%Y-%m-%d') - datetime..timedelta(days=1)).strftime("%Y-%m-%d") # Create 1-day windows for extraction
        fromDate = dates[i] 
        toDate = dates[i+1]
        result = api.search.tweets(q=query + f" AND since:{fromDate} until:{toDate}", count=100 )
        print(json.dumps(result, indent=1))
        save_tweets(clean_results(result, topic))
        result_count = result["search_metadata"]["count"]
        next_max_id = result["search_metadata"]["next_results"].split('max_id=')[1].split('&')[0]
        while result_count < count:
            result = api.search.tweets(q=query, include_entities='true',max_id=next_max_id, count=100,  fromDate=fromDate, toDate=toDate)
            print(result["search_metadata"])
            print(result_count)
            save_tweets(clean_results(result, topic))
            result_count += result["search_metadata"]["count"]
            if "next_results" in result["search_metadata"]:
                next_max_id = result["search_metadata"]["next_results"].split('max_id=')[1].split('&')[0]
            else:
                break
        
def main():
    try:
        
        # topics = ["ModernaVaccine","JohnsonAndJohnsonVaccine", "PfizerVaccine"]
        topics = ["Vaccine"]
        list_of_dates = []
        today = datetime.date.today()
        for i in range(-7,1):
            target_date = (today + datetime.timedelta(days=i)).isoformat()
            list_of_dates.append(target_date)
        print(list_of_dates)

        for topic in topics:
            query_tweet("#"+ topic+" -RT AND lang:en", 2000, topic, list_of_dates)
            # print(json.dumps(result, indent=1))
            print("Done writing"+topic)            
    except Exception as e:
        print(e)

main()