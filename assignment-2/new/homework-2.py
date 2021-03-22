'''
CIS-600 - Social Media and Data Mining, Assignment 2
Author: Swapnil Ghanshyam Deshaware
SUID: 253579042
Assignment - Social Network Generation for a Twitter user
'''

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


def get_user_profile(api, screen_names=None, user_ids=None):
    '''
    This method helps getting user profile by id or name
    This method is referred from the Twitter Cookbook
    '''
    assert (screen_names != None) != (user_ids != None), "Must have screen_names or user_ids, but not both"
    items_to_info = {}
    items = screen_names or user_ids
    
    while len(items) > 0:

        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]

        if screen_names:
            response = make_twitter_request(api.users.lookup, 
                                            screen_name=items_str)
        else: # user_ids
            response = make_twitter_request(api.users.lookup, 
                                            user_id=items_str)
    
        for user_info in response:
            if screen_names:
                items_to_info[user_info['screen_name']] = user_info
            else: # user_ids
                items_to_info[user_info['id']] = user_info

    return items_to_info

def pretty_print(data):
    '''
    To print the data in readable json format
    '''
    print(json.dumps(data, sort_keys=True, indent=1))

def get_friends_followers_ids(api, screen_name=None, user_id=None,
                              friends_limit=maxint, followers_limit=maxint):
    '''
    The function takes twitter api input of a user and and returns friends and followers
    This function is taken from the twitter cookbook
    '''

    assert (screen_name != None) != (user_id != None), "Must have screen_name or user_id, but not both"
    
    get_friends_ids = partial(make_twitter_request, api.friends.ids, count=5000)
    get_followers_ids = partial(make_twitter_request, api.followers.ids, count=5000)
    friends_ids, followers_ids = [], []
    for api_func, limit, ids, label in [
                    [get_friends_ids, friends_limit, friends_ids, "friends"], 
                    [get_followers_ids, followers_limit, followers_ids, "followers"]
                ]:
        if limit == 0: continue
        
        cursor = -1
        while cursor != 0:
        
            # Use make_twitter_request via the partially bound callable...
            if screen_name: 
                response = api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id
                response = api_func(user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
        
            print('Fetched {0} total {1} ids for {2}'.format(len(ids),label, (user_id or screen_name)),file=sys.stderr)
            if len(ids) >= limit or response is None:
                break

    return friends_ids[:friends_limit], followers_ids[:followers_limit]

def get_top_followers(api, all_followers):
    '''
    Get the top connections who has highest of followers
    '''
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

def get_top_5_reciprocal_friends(api, ID):
    '''
    Get top 5 reciprocal friends for given argument ID
    This function provides top 5 reciprocal friends which are followers and friends
    of the given user ID
    '''
    friends_ids, followers_ids = get_friends_followers_ids(api,
                                                    user_id = ID, 
                                                    friends_limit=50, 
                                                    followers_limit=50)
    return get_top_followers(api, set(friends_ids) & set(followers_ids))

def crawl_followers(api, graph_obj, screen_name, minimum_limit=100, depth=2):
    '''
    This method crawls the followers and creates a network until we reach node 100
    The logic behind this implementation is based on the queue, which takes top 5 reciprocal friends
    of the node and create edges between them, if the node has child already, it will 
    '''
    user_info = make_twitter_request(api.users.show, screen_name=screen_name)
    ID = user_info['id']
    network_graph = []
    unique_friends = []
    #dictionary to store information about nodes and the edges
    network_dict = {}
    next_queue = get_top_5_reciprocal_friends(api, ID)
    network_dict.update({ID : list(next_queue)})
    network_graph.append(ID)
    network_graph.extend(list(next_queue.keys())) 
    graph_obj.add_a_node(ID)
    graph_obj.add_node(list(next_queue.keys()))
    for n in list(next_queue.keys()):
        graph_obj.add_a_edge((ID,n))
    d = 1
    #initiating the queue with a user's top 5 reciprocal friends
    next_queue_list = list(next_queue.keys())
    while len(network_graph) < minimum_limit :
        print("Size of the graph is : ", len(network_graph))
        d += 1
        (queue, next_queue_list) = (list(set(next_queue_list)), [])
        for fid in queue:
            top_5_reciprocal_friends = get_top_5_reciprocal_friends(api,fid)
            
            #calculate unique friends and add them into the network graph
            unique_friends = list(set(top_5_reciprocal_friends) - set(network_graph))
            print("Friends", unique_friends)
            print("network_graph size is", len(network_graph))
            print("network_dict size is", len(network_dict))
            network_graph += unique_friends
            #adding new nodes to graph
            graph_obj.add_node(unique_friends)
            for n in top_5_reciprocal_friends:
                graph_obj.add_a_edge((fid,n))
            
            #Update the dictionary based on the unique node found
            network_dict.update({fid : unique_friends})
            next_queue_list +=  unique_friends
            if(len(network_dict) > minimum_limit):
                return network_dict
            if(len(network_graph) > minimum_limit):
                return network_dict
    return network_dict

class Graph:
    '''
    The graph class helps with a networkx object to create a graph.
    It uses BFS(Breadth First Search) to create nodes and edges to form a network
    '''
    def __init__(self):
        self.network_graph = networkx.Graph()

    # Add nodes 
    def add_node(self, node_list):
        self.network_graph.add_nodes_from(node_list)

    # Add a node to the existing graph 
    def add_a_node(self, node):
        self.network_graph.add_node(node)

    #Add edges from a list to the existing graph 
    def add_edge(self, edge_list):
        self.network_graph.add_edges_from(edge_list)

    # Add a edge to the existing graph 
    def add_a_edge(self, edge):
        self.network_graph.add_edge(*edge)

    # Display the graph information on the console
    def display_graph(self):
        '''
        This method belongs to class Graph and used for displaying the graph
        '''
        file = open("FinalOutputFile.txt","w") 

        file.write("\nNumber of Nodes : " + str(self.network_graph.number_of_nodes())) 
        print("Number of nodes : ", self.network_graph.number_of_nodes())

        file.write("\nNumber of of Edges : " + str(self.network_graph.number_of_edges()))
        print("Number of edges : : ",self.network_graph.number_of_edges())

        file.write("\n Diameter : " + str(networkx.diameter(self.network_graph, e=None, usebounds=False)))
        print("Diameter : " , networkx.diameter(self.network_graph, e=None, usebounds=False))

        file.write("\nAverage distance : " +  str(networkx.average_shortest_path_length(self.network_graph, weight=None)))
        print("Average distance : " , networkx.average_shortest_path_length(self.network_graph, weight=None))

        file.close() 
        networkx.draw(self.network_graph, with_labels=True)
        plt.savefig('output.png', bbox_inches=0, orientation='landscape', pad_inches=0.5)
        plt.show()



if __name__ == '__main__':
    try:
        api = oauth_login()
        print("\n\nTask-1: ")
        print("Name:", NAME)
        print("username ", USERNAME)

        print("Current User Description")
        pretty_print(make_twitter_request(api.users.show,user_id=ID)["description"])

        print("\n\nTask-2: ")
        followers =  make_twitter_request(api.followers.ids, user_id=ID,count=5000)
        friends = make_twitter_request(api.friends.ids, user_id=ID,count=5000)

        print("Followers", followers["ids"])
        print("\nFriends", friends["ids"])

        reciprocal_friends = set(followers["ids"]) & set(friends["ids"])
        reciprocal_friends = [i for i in reciprocal_friends]
        print("\n\nTask-3 Distance-1 Reciprocal Friends")
        print("\nReciprocal Friends", reciprocal_friends)

        user_profiles = get_user_profile(api,user_ids=list(reciprocal_friends))

        #sort
        user_profiles_data = [ j for i,j in user_profiles.items()]
        newlist = sorted(user_profiles_data, key=itemgetter('followers_count'), reverse=True)
        top_user_profiles = newlist[:5]
        print("\n\nTask-4 Most Popular Reciprocal Friends")
        print([i["id"] for i in top_user_profiles])

        print("\n\nTask-5 and Task-6: Crawling Followers and create network for ", USERNAME)
        print("\nCreating a network for 'distance-1', 'distance-2' and so on ")
        graph = Graph()
        crawl_followers(api, graph, screen_name = USERNAME, minimum_limit=100, depth = 10)

        print("\n\nTask-7: ")
        print("\nBuilding a network based on task-5")
        graph.display_graph()

    except RuntimeError as e:
        print("error", e)