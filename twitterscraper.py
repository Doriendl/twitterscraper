import twitter
import csv

# == To be allowed to scrape tweets, you have to give your consumer-secret, access-token and Access_token_secret, which are completely personal, so better not put it in a public space
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""


AUTH = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
TWITTER_API = twitter.Twitter(auth=AUTH)

# Here is the first row created for the csv file: all the categories that will be collected later on from the tweets.
# it first opens a new csv file and then writes the different categories to it.
csvfile = open('all_users_tweets.csv', 'w')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['created_at',
                    'user-screen_name',
                    'text',
                    'coordinates lng',
                    'coordinates lat',
                    'place',
                    'user-location',
                    'user-geo_enabled',
                    'user-lang',
                    'user-time_zone',
                    'user-statuses_count',
                    'user-followers_count',
                    'user-created_at'])

# Get user ID's here http://gettwitterid.com/
# I have put in this line all the twitter ID's from the nezsroom at De Tijd.
TWITTER_USER_IDS = '2882657302,219337111,96795420,21858309,17710420,157284794,27618586,158375371,255534811,230209323,166149287,198953451,8795292,229048913,150792051,56470826,29182017,155858628,226184788,52546907,17892379,389393869,589299475,31103332,8781942,8872972,483847400,2595341161,246366488,211179530,307791468,964162182,17242884,229048820,141174185,155924014,301941982,19022119,25989332,8744472,23427849,158363528,1735171,65982083,8784242,8935252,7504712,229048865,258074147,152959566,2261541074,239764726,117717712,18672805,341507145,477110053,31102880,94433208,158366047,222583264,1595464278'

twitter_stream = twitter.TwitterStream(auth=TWITTER_API.auth)
stream = twitter_stream.statuses.filter(_method="POST", follow=TWITTER_USER_IDS)

#These are helper functions for tweet data, clean up utf data and unpack dictionaries. '''
def getVal(val):
    clean = ""
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return val
    if val:
        clean = val.encode('utf-8') 
    return clean

def getLng(val):
    if isinstance(val, dict):
        return val['coordinates'][0]

def getLat(val):
    if isinstance(val, dict):
        return val['coordinates'][1]

def getPlace(val):
    if isinstance(val, dict):
        return val['full_name'].encode('utf-8')


# this is the loop to get the different data from the tweets from the accounts. A loop repeats itself until it reaches its end or if someone stops it. 
# All the bits of data collected are then written into a csv file that can be analysed later on. 
# The different categories here follow the same order as earlier, so they end up under the correct category name
for tweet in stream:
    try:
        csvwriter.writerow([tweet['created_at'],
                            getVal(tweet['user']['screen_name']),
                            getVal(tweet['text']),
                            getLng(tweet['coordinates']),
                            getLat(tweet['coordinates']),
                            getPlace(tweet['place']),
                            getVal(tweet['user']['location']),
                            getVal(tweet['user']['geo_enabled']),
                            getVal(tweet['user']['lang']),
                            getVal(tweet['user']['time_zone']),
                            getVal(tweet['user']['statuses_count']),
                            getVal(tweet['user']['followers_count']),
                            getVal(tweet['user']['created_at'])
                            ])
        csvfile.flush()
