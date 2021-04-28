from textblob import TextBlob

# text = "I got my 2nd microchip today! So far I'm not getting any signal! I'll let you know"
# text = "Received my 2nd Moderna COVID shot a week ago.  I have horrible upper back pain which started two days after the s"
# text = "This year is very beautiful with my gorgeous girl. The roommate is horrible, pathetic piece of work, but I am awesome and friendly"
text= "This girl is one of the most stupid person i've ever seen and she is super horrible and dumb "

'''
The titular threat of The Blob has always struck me as the ultimate movie
monster: an insatiably hungry, amoeba-like mass able to penetrate
virtually any safeguard, capable of--as a doomed doctor chillingly
describes it--"assimilating flesh on contact.
Snide comparisons to gelatin be damned, it's a concept with the most
devastating of potential consequences, not unlike the grey goo scenario
proposed by technological theorists fearful of
artificial intelligence run rampant.
'''

blob = TextBlob(text)
blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                    #  ('threat', 'NN'), ('of', 'IN'), ...]

blob.noun_phrases   # WordList(['titular threat', 'blob',
                    #            'ultimate movie monster',
                    #            'amoeba-like mass', ...])

for sentence in blob.sentences:
    print(sentence.sentiment.polarity)