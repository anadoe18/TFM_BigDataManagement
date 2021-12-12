#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install tweepy')
get_ipython().system('pip install textblob')
get_ipython().system('pip install pycountry')
get_ipython().system('pip install langdetect')
get_ipython().system('pip install pandas')
get_ipython().system('pip install sklearn')


# In[ ]:


conda install -c conda-forge wordcloud=1.6.0 


# In[2]:


# Import Libraries

from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
nltk.download('vader_lexicon')
nltk.download('stopwords')
import pycountry
import re
import string

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


# In[3]:


# Authentication
consumerKey = "a0cLYyjRSHFcXcTTU7RvYGgHh"
consumerSecret = "uQVZt6LIcgporqJ3iAjDpehFufKgAfqYzPpbreIEHUcN70rXPw"
accessToken = "1461438773078769666-uAYj5L4fiB5lzA0T5fj1VtW5gdckie"
accessTokenSecret = "UBGFL3v5kFJZm8VTXMoecGQ2eerYteQ3rRa4ia7vVbX2b"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


# In[58]:


#Sentiment Analysis

def porc(part,whole):
    return 100 * float(part)/float(whole) 

palabraclave = input("Keyword")
numeroTweets = int(input ("NºTweets"))


tweets = tweepy.Cursor(api.search_tweets, q=palabraclave).items(numeroTweets)
positivos  = 0
negativos = 0
neutros = 0
polaridad = 0
lista_tweets = []
lista_neutros = []
lista_negativos = []
lista_positivos = []

for tweet in tweets:
    
    #print(tweet.text)
    lista_tweets.append(tweet.text)
    analysis = TextBlob(tweet.text)
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    negativo = score['neg']
    neutro = score['neu']
    positivo = score['pos']
    compuesto = score['compound']
    polarity += analysis.sentiment.polarity
    
    if negativo > positivo:
        lista_negativos.append(tweet.text)
        negativos += 1

    elif positivo > negativo:
        lista_positivos.append(tweet.text)
        positivos += 1
    
    elif positivo == negativo:
        lista_neutros.append(tweet.text)
        neutros += 1

positivos = porc(positivos, numeroTweets)
negativos = porc(negativos, numeroTweets)
neutros = porc(neutros, numeroTweets)
polaridad = porc(polaridad, numeroTweets)
positivos = format(positivos, '.1f')
negativos = format(negativos, '.1f')
neutros = format(neutros, '.1f')


# In[59]:


#Number of Tweets (Total, Positive, Negative, Neutral)
lista_tweets = pd.DataFrame(lista_tweets)
lista_neutros = pd.DataFrame(lista_neutros)
lista_negativos = pd.DataFrame(lista_negativos)
lista_positivos = pd.DataFrame(lista_positivos)
print("numero total tweets: ",len(lista_tweets))
print("tweets positivos: ",len(lista_positivos))
print("tweets negativos: ", len(lista_negativos))
print("tweets neutros: ",len(lista_neutros))


# In[60]:


lista_tweets


# In[62]:


#Creating PieCart

labels = ['Positivos ['+str(positive)+'%]' , 'Neutros ['+str(neutral)+'%]','Negativos ['+str(negative)+'%]']
sizes = [positivos, neutros, negativos]
colors = ['yellowgreen', 'blue','red']
patches, texts = plt.pie(sizes,colors=colors, startangle=90)
plt.style.use('default')
plt.legend(labels)
plt.title("Analisis de sentimientos  "+keyword+"" )
plt.axis('equal')
plt.show()


# In[63]:


lista_tweets.drop_duplicates(inplace = True)


# In[65]:


lista_tweets_a_limpiar = pd.DataFrame(lista_tweets)
lista_tweets_a_limpiar["text"] = lista_tweets_a_limpiar[0]
lista_tweets_a_limpiar


# In[66]:


lista_tweets


# In[67]:


#Cleaning Text (RT, Punctuation etc)

#Creating new dataframe and new features
lista_tweets_a_limpiar = pd.DataFrame(tweet_list)
lista_tweets_a_limpiar["text"] = lista_tweets_a_limpiar[0]

#Removing RT, Punctuation etc
remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
rt = lambda x: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x)
lista_tweets_a_limpiar["text"] = tw_list.text.map(remove_rt).map(rt)
lista_tweets_a_limpiar["text"] = tw_list.text.str.lower()
lista_tweets_a_limpiar.head(10)


# In[68]:


#Calculating Negative, Positive, Neutral and Compound values

lista_tweets_a_limpiar[['polarity', 'subjectivity']] = lista_tweets_a_limpiar['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
for i, r in lista_tweets_a_limpiar['text'].iteritems():
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    negativos = score['neg']
    nuetros = score['neu']
    positivos = score['pos']
    compuestos = score['compound']
    if negativos > positivos:
        lista_tweets_a_limpiar.loc[index, 'sentiment'] = "negativos"
    elif positivos > negativos:
        lista_tweets_a_limpiar.loc[index, 'sentiment'] = "positivos"
    else:
        lista_tweets_a_limpiar.loc[index, 'sentiment'] = "neutros"
    lista_tweets_a_limpiar.loc[index, 'neg'] = negativos
    lista_tweets_a_limpiar.loc[index, 'neu'] = neutros
    lista_tweets_a_limpiar.loc[index, 'pos'] = positivos
    lista_tweets_a_limpiar.loc[index, 'compound'] = compuestos

lista_tweets_a_limpiar.head(10)


# In[79]:


#Creating new data frames for all sentiments (positive, negative and neutral)

lista_negativos_v2 = lista_tweets_a_limpiar[lista_tweets_a_limpiar["sentiment"]=="negativos"]
lista_positivos_v2 = lista_tweets_a_limpiar[lista_tweets_a_limpiar["sentiment"]=="positivos"]
lista_neutros_v2 = lista_tweets_a_limpiar[lista_tweets_a_limpiar["sentiment"]=="neutros"]


# In[80]:


#Function for count_values_in single columns

def count_values_in_column(data,feature):
    total=data.loc[:,feature].value_counts(dropna=False)
    percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Porcentage'])


# In[81]:


#Count_values for sentiment
count_values_in_column(lista_tweets_a_limpiar,"sentiment")


# In[82]:


#Function to Create Wordcloud

def contador_palabras(text):
    stopwords = set(STOPWORDS)
    cont_pal = WordCloud(background_color="white",
                  max_words=3000,
                  stopwords=stopwords,
                  repeat=True)
    cont_pal.generate(str(text))
    cont_pal.to_file("imagen_contador_palabras.png")
    path="imagen_contador_palabras.png"
    display(Image.open(path))


# In[83]:


#Creating wordcloud for all tweets
contador_palabras(lista_tweets_a_limpiar["text"].values)


# In[85]:


#Creating wordcloud for positive sentiment
contador_palabras(lista_positivos_v2["text"].values)


# In[47]:


#Creating wordcloud for negative sentiment
contador_palabras(lista_negativos_v2["text"].values)


# In[48]:


#Creating wordcloud for neutral sentiment
contador_palabras(lista_neutros_v2["text"].values)


# In[49]:


#Calculating tweet's lenght and word count
lista_tweets_a_limpiar['text_len'] = lista_tweets_a_limpiar['text'].astype(str).apply(len)
lista_tweets_a_limpiar['text_word_count'] = lista_tweets_a_limpiar['text'].apply(lambda x: len(str(x).split()))


# In[50]:


round(pd.DataFrame(lista_tweets_a_limpiar.groupby("sentiment").text_len.mean()),2)


# In[ ]:




