import tweepy
import pandas as pd
from textblob import TextBlob #for doing sentiment analysis
import numpy as np
import re #for cleaning text
import matplotlib.pyplot as plt
from data.models import Comment
from pprint import pprint
import sqlalchemy

def clean(x):
 x = re.sub(r'^RT[\s]+', '', x)
 x = re.sub(r'https?:\/\/.*[\r\n]*', '', x)
 x = re.sub(r'#', '', x)
 x = re.sub(r'@[A-Za-z0–9]+', '', x)
 return x

def ratio(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1
# insert comments from the data
def insertComment(arg1,arg2,data):
    # get the dataframe object you want to insert into database
    comments = arg1.loc[arg1.analysis == -1, ['tweet','time','analysis']] 
    # rename columns of dataframe here
    comments.rename(columns={
        'tweet' : 'comment',
        'time':'created_at'

    }, inplace = True)
    # creating dataframe fro data id
    d = []
    for i in range(comments.analysis.size):
        d.append(data.id)
    # the series of data id i.e pd.series(d) is converted to dataframe here 
    analy = comments.analysis
    analy_array =   analy.to_numpy()
    # # this dataid and analysisid dataframe 
    data_analy = pd.DataFrame({'data_id':d, 'analysis':analy_array}, columns=['data_id','analysis'])
    # # merger the dataframe with the main comment dataframe
    comments_m = pd.merge(comments, data_analy, on='analysis')
    # # sql engine for the insertion
    engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/empanalyst')
   
    comments_m.to_sql('data_comment', con=engine, index=False, if_exists = 'append')
    
def generateData(key_word,clean):
    consumer_key = 'vr0xOp7U4aPvVxMQvBRKa366v'
    consumer_secret = 'AFhsqFeAyogygjkt7nN0ftgEu9toxGphruiih2JW8kIU0luONU'
    access_token = '1147160132062797830-LW8kJ3KL4AM0VKn1bL7G6uDTmlD5P1'
    access_token_secret = 'OxjJB8y8nFolnMEE1AL7kQfwNMHG5rDeBkm7Q88q9KvAG'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # Get related twitter data
    twitter_users = []
    tweet_time = []
    tweet_string = []
    for tweet in tweepy.Cursor(api.search,q=key_word, rpp=100,count=1000, goecode='9.0820° N, 8.6753° E', show_user='true').items(1000):
            if (not tweet.retweeted) and ('RT @' not in tweet.text):
                if tweet.lang == "en":
                    twitter_users.append(tweet.user.name)
                    tweet_time.append(tweet.created_at)
                    tweet_string.append(tweet.text)
                    #print([tweet.user.name,tweet.created_at,tweet.text])
    df = pd.DataFrame({'name':twitter_users, 'time': tweet_time, 'tweet': tweet_string})
    df['tweet'] = df['tweet'].apply(clean)
    df.to_csv(f"uploads/{key_word}.csv")
    return df



def analyseData(df,ratio,data):
    polarity = lambda x: TextBlob(x).sentiment.polarity
    subjectivity = lambda x: TextBlob(x).sentiment.subjectivity
    df['polarity'] = df['tweet'].apply(polarity)
    df['subjectivity'] = df['tweet'].apply(subjectivity)
    plt.rcParams['figure.figsize'] = [10, 8]
    for index, Tweets in enumerate(df.index):
        x = df.polarity.loc[Tweets]
        y = df.subjectivity.loc[Tweets]
        plt.scatter(x, y, color=("red"))

    plt.title('Empowerment Data Analysis result', fontsize = 20)
    plt.xlabel('← Negative — — — — — — Positive →', fontsize=15)
    plt.ylabel('← Facts — — — — — — — Opinions →', fontsize=15)
    plt.show()
    df['analysis'] = df['polarity'].apply(ratio)
    # result = insertComment(df,Comment,data)
    df['analysis'].value_counts().plot(kind = 'bar')
    plt.show()
# plt.show()
    # print(df['analysis'].value_counts())

# Creating function for calculating positive, negative and neutral
# More than 1 --> Positive, equal to 0 --> neutral and less than 0 --> Negative





#Plotting
#