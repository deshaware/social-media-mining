import twitter
import json
import networkx
import matplotlib.pyplot as plt
import sys
import time
from urllib.error import URLError
from operator import itemgetter
from functools import partial
from sys import maxsize as maxint
from http.client import BadStatusLine

ID="141631266"
NAME="Swapnil Deshaware"
USERNAME="_arsenalistq"
MAX_FRIENDS=5000
MAX_FOLLOWERS=5000
MAX_NODES=100

def oauth_login():
    '''
    A static method to authenticate user
    '''
    #mine
    CONSUMER_KEY = 'agQmGHFcg9CDeoUSXUFvdPllT'
    CONSUMER_SECRET = 'N9rqHRmzCJt4SALlxWOCbYyXno0khHnbFTwBFVnrqEKWA1VlfL'
    BEARER_TOKEN= "AAAAAAAAAAAAAAAAAAAAAE04NwEAAAAAjQ9nJ%2BLef%2Fkj3cM1txJPOBATLJk%3DisQRS6PBXd5VLdOFUFgirQpkoK5oygGUbLMku7G0vYetzIyYJt"
    
    auth = twitter.OAuth2(CONSUMER_KEY, CONSUMER_SECRET, BEARER_TOKEN)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def get_user(twitter_api, id):
    user = twitter_api.users.show(user_id=id)
    return user

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
    
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
    
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e
    
        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes
    
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
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'                  .format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function
    
    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
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


def get_user_profile(twitter_api, screen_names=None, user_ids=None):
       
    # Must have either screen_name or user_id (logical xor)
    assert (screen_names != None) != (user_ids != None),     "Must have screen_names or user_ids, but not both"
    
    items_to_info = {}

    items = screen_names or user_ids
    
    while len(items) > 0:

        # Process 100 items at a time per the API specifications for /users/lookup.
        # See    for details.
        
        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]

        if screen_names:
            response = make_twitter_request(twitter_api.users.lookup, 
                                            screen_name=items_str)
        else: # user_ids
            response = make_twitter_request(twitter_api.users.lookup, 
                                            user_id=items_str)
    
        for user_info in response:
            if screen_names:
                items_to_info[user_info['screen_name']] = user_info
            else: # user_ids
                items_to_info[user_info['id']] = user_info

    return items_to_info

def get_friends(api, id):
    return api.friends.ids(user_id=id,count=5000)

def get_followers(api, id):
    return api.followers.ids(user_id=id, count=5000)

def pretty_print(data):
    print(json.dumps(data, sort_keys=True, indent=1))

def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
                              friends_limit=maxint, followers_limit=maxint):
    
    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None),     "Must have screen_name or user_id, but not both"
    
    # See http://bit.ly/2GcjKJP and http://bit.ly/2rFz90N for details
    # on API parameters
    
    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids, count=5000)
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids, count=5000)

    friends_ids, followers_ids = [], []
    
    for twitter_api_func, limit, ids, label in [
                    [get_friends_ids, friends_limit, friends_ids, "friends"], 
                    [get_followers_ids, followers_limit, followers_ids, "followers"]
                ]:
        
        if limit == 0: continue
        
        cursor = -1
        while cursor != 0:
        
            # Use make_twitter_request via the partially bound callable...
            if screen_name: 
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id
                response = twitter_api_func(user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
        
            print('Fetched {0} total {1} ids for {2}'.format(len(ids),label, (user_id or screen_name)),file=sys.stderr)
        
            # XXX: You may want to store data during each iteration to provide an 
            # an additional layer of protection from exceptional circumstances
        
            if len(ids) >= limit or response is None:
                break

    # Do something useful with the IDs, like store them to disk...
    return friends_ids[:friends_limit], followers_ids[:followers_limit]

def get_top_followers(api, all_followers):
    top_followers = {}
    for follower in all_followers:
        followers_info = get_user_profile(api, user_ids = [follower])
        top_followers.update({followers_info[follower]["id"] : followers_info[follower]["followers_count"]})
    if(len(top_followers) >= 5):
        min_value = sorted(top_followers.values(), reverse=True)[4]
    elif(len(top_followers) > 1):
        min_value = sorted(top_followers.values(), reverse=True)[len(top_followers)-1]
    else:
        min_value = 0
    top_followers = {key:value for key,value in top_followers.items() if value >= min_value}
    return top_followers

def get_top_5_reciprocal_friends(api, id):
    friends_ids, followers_ids = get_friends_followers_ids(api,
                                                    user_id = id, 
                                                    friends_limit=50, 
                                                    followers_limit=50)
    return get_top_followers(api, set(friends_ids) & set(followers_ids))

def crawl_followers(api, graph_obj, screen_name, minimum_limit=100, depth=2):
        user_info = make_twitter_request(api.users.show, screen_name=screen_name)
        id = user_info['id']

        connection_dictionary = {}
        connection_graph_list = []
        unique_friends = []
        next_queue = get_top_5_reciprocal_friends(api, id)
        connection_dictionary.update({id : list(next_queue)})
        connection_graph_list.append(id)
        connection_graph_list.extend(list(next_queue.keys())) 
        graph_obj.add_a_node(id)
        graph_obj.add_node(list(next_queue.keys()))
        for n in list(next_queue.keys()):
            graph_obj.add_a_edge((id,n))
        d = 1
        next_queue_list = list(next_queue.keys())
        while len(connection_graph_list) < minimum_limit :
            print("Size of the graph is : ", len(connection_graph_list))
            d += 1
            (queue, next_queue_list) = (list(set(next_queue_list)), [])
            for fid in queue:
                top_5_reciprocal_friends = get_top_5_reciprocal_friends(api,fid)
                
                unique_friends = list(set(top_5_reciprocal_friends) - set(connection_graph_list))
                print("Friends", unique_friends)
                print("connection_graph_list size is", len(connection_graph_list))
                print("connection_dictionary size is", len(connection_dictionary))
                connection_graph_list += unique_friends
                #adding new nodes to graph
                graph_obj.add_node(unique_friends)
                for n in top_5_reciprocal_friends:
                    graph_obj.add_a_edge((fid,n))
                connection_dictionary.update({fid : unique_friends})
                next_queue_list +=  unique_friends
                if(len(connection_dictionary) > minimum_limit):
                    return connection_dictionary
                if(len(connection_graph_list) > minimum_limit):
                    return connection_dictionary
        return connection_dictionary

class Graph:
    
    #--------------< Constructor of the class to define the sn = social network graph >-----------------
    def __init__(self):
        self.network_graph = networkx.Graph()

    #--------------< Add nodes from a list to the existing graph >-----------------
    def add_node(self, node_list):
        self.network_graph.add_nodes_from(node_list)

    #--------------< Add a node to the existing graph >-----------------
    def add_a_node(self, node):
        self.network_graph.add_node(node)

    #--------------< Add edges from a list to the existing graph >-----------------
    def add_edge(self, edge_list):
        self.network_graph.add_edges_from(edge_list)

    #--------------< Add a edge to the existing graph >-----------------
    def add_a_edge(self, edge):
        self.network_graph.add_edge(*edge)

    #--------------< Display the graph information on the console >-----------------
    def display_graph(self):
        file = open("FinalOutputFile.txt","w") 

        file.write("\nSize of Network in terms of Nodes : " + str(self.network_graph.number_of_nodes())) 
        print("Network size in terms of nodes : ", self.network_graph.number_of_nodes())

        file.write("\nSize of Network in terms of Edges : : " + str(self.network_graph.number_of_edges()))
        print("Network size in terms of edges : : ",self.network_graph.number_of_edges())

        file.write("\nSize of Network in terms of Diameter : " + str(networkx.diameter(self.network_graph, e=None, usebounds=False)))
        print("Network size in terms of Diameter : " , networkx.diameter(self.network_graph, e=None, usebounds=False))

        file.write("\nSize of Network in terms of Average distance : " +  str(networkx.average_shortest_path_length(self.network_graph, weight=None)))
        print("Network size in terms of Average distance : " , networkx.average_shortest_path_length(self.network_graph, weight=None))

        file.close() 
        networkx.draw(self.network_graph, with_labels=True)
        plt.savefig('output.png', bbox_inches=0, orientation='landscape', pad_inches=0.5)
        plt.show()



if __name__ == '__main__':
    api = oauth_login()
    try:
        followers = get_followers(api, ID)
        # pretty_print(followers["ids"])
        friends = get_friends(api, ID)
        # pretty_print(friends)
        followers["ids"]

        reciprocal_friends = set(followers["ids"]) & set(friends["ids"])
        reciprocal_friends = [i for i in reciprocal_friends]

        print(reciprocal_friends.pop())
        print(reciprocal_friends)
        # top 5 reciprocal friends

        #get profile
        user_profiles = get_user_profile(api,user_ids=list(reciprocal_friends))
        # for i in user_profiles:
        #     print(user_profiles[i]["screen_name"], " ", user_profiles[i]["followers_count"])
        
        #sort
        user_profiles_data = [ j for i,j in user_profiles.items()]
        newlist = sorted(user_profiles_data, key=itemgetter('followers_count'), reverse=True)
        top_user_profiles = newlist[:5]

        print("\n\nSolution for task-5: ")
        print("\nMoving to the friends of user who are at 'distance-1', 'distance-2' etc form a network")
        graph = Graph()
        crawl_followers(api, graph, screen_name = USERNAME, minimum_limit=100, depth = 10)

        print("\n\nSolution for task-6: ")
        print("\nCreating a social network based on the results from Req 5")
        graph.display_graph()

    except RuntimeError as e:
        print("error", e)
    



    



    