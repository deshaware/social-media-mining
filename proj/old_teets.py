import GetOldTweets3 as got

tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#PfizerVaccine -RT')\
                                           .setSince("2021-03-01")\
                                           .setUntil("2021-03-30")\
                                           .setMaxTweets(10)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)