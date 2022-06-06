import urllib.request,sys,time
from bs4 import BeautifulSoup
import requests
import pandas as pd

from tqdm import tqdm
import nltk
from nltk.tokenize import WordPunctTokenizer as wpt
from textblob import TextBlob
import plotly.graph_objects as pgo
import plotly.express as px



URL = 'https://www.aljazeera.com/where/mozambique/'





page = requests.get(URL)

#Getting articles which are featured in the top container of the URL
soup = BeautifulSoup(page.text, "html.parser")
links = soup.find_all('li', attrs = {'class': 'featured-articles-list__item'})


#Getting the remaining articles from the bottom container as we need a total of 10 pages
remaining_links = soup.find_all('article', attrs = {'class': 'gc u-clickable-card gc--type-post gc--list gc--with-image'})

#Here we only get a specific number of articles required to fulfill the length of articles as 10
new_r = remaining_links[0:6]    
combined_links = links + new_r


# Here we iterate through the bs4.Tag elements to extract only the content and title from them and adding them to a list so as to create a pandas DF
upperframe = []
frame = []
for j in tqdm(combined_links):
    
    #Getting the title of the article only for gist purposes. CLeaning text as well by replacing hexcode characters with null
    Title = j.find('div', attrs={'class':'gc__content'}).find('a').get_text(strip= True).replace('\xad','')
    
    #URL only contains links to 10 articles. We need to extract content from them. Getting href from <a> tag and creating a specific article URl
    newlink = 'https://www.aljazeera.com' + j.find('a', attrs ={'class':'u-clickable-card__link'}).get('href')
    page = requests.get(newlink)
    soup = BeautifulSoup(page.text, "html.parser")
    
    #after getting to the page with bs4, now we extract the content which is in the <div> tag with all-content class
    Text = soup.find('div', attrs = {'class': "wysiwyg wysiwyg--all-content css-1ck9wyi"}).get_text(strip = True)
    
    frame.append([Title,Text])
upperframe.extend(frame)

#Creating a pandas DF with upperframe list and setting appropriate column names
data=pd.DataFrame(upperframe)
data.columns = ['Title','Content']



#Let's try TexTBlob library to get the scores of the content
article_text = TextBlob(data['Content'][1])
print(article_text.sentiment)

#Since the scores are very low(scale of polarity is between -1 and 1 where 1 indicates Positive and -1 indicates Negative)
# We will try another way to get the sentiment of articles which includes counting the number of positive and negative words and deciding based on those values the sentiment of the content
data['Sentiment'] = ''
for i in tqdm(range(len(data))):
    
    #first we need to tokenize the data and make it lowercase so that python will know that 'A' and 'a' mean the same while calculating sentiment value
    words = wpt().tokenize(data['Content'][i])
    words = [word.lower() for word in words]
    
    #Now we remove the stopwords from the content so we can get more accurate sentiment
    stopwords = nltk.corpus.stopwords.words('english')
    words_new = [word for word in words if word not in stopwords]
    
    #To get the score of positive or negative we see if the word in our df is present in the Loughran-McDonald Master Dictionary
    master = pd.read_csv("Loughran-McDonald_MasterDictionary_1993-2021.csv")
    positive = master[master["Positive"]>0]
    negative = master[master["Negative"]>0]

    #Converting to list
    pos_words = positive["Word"].tolist()
    neg_words = negative["Word"].tolist()

    pos_words = [word.lower() for word in pos_words]
    neg_words = [word.lower() for word in neg_words]

    #Getting the words in their appropriate lists
    words_new_pos = [word for word in words_new if word in pos_words]
    words_new_neg = [word for word in words_new if word in neg_words]
        
    
    #If difference between number of positive and negative words is less than 1 then the sentiment is Neutral.
    #If count of positive words is higher than negative then sentiment is Positive, else negative
    if abs(len(words_new_neg)- len(words_new_pos)) <=1:
        data['Sentiment'][i]  = 'Neutral'
    elif len(words_new_pos) > len(words_new_neg):
        data['Sentiment'][i]  = 'Positive'
    elif  len(words_new_pos) < len(words_new_neg):
        data['Sentiment'][i] = 'Negative'



#Using Plotly to make histogram, Scatterplot and a combination of both with dropdown menu
import plotly.express as px

fig = px.histogram(data, x="Sentiment", color = 'Sentiment', barmode= 'group')
#fig.show()
fig.write_html("histogram.html")


fig = px.scatter(data, x="Sentiment", color = 'Sentiment', hover_name='Title')
fig.update_traces(marker_size=20)
#fig.show()
fig.write_html("scatter.html")



plot = pgo.Figure(data=[pgo.Scatter(
    x=data['Sentiment'],
    mode='markers',)
])
 
# Add dropdown
plot.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=["type", "scatter"],
                    label="Scatter Plot",
                    method="restyle"
                ),
                dict(
                    args=["type", "histogram"],
                    label="Histogram",
                    method="restyle"
                )
            ]),
        ),
    ]
)
 
#plot.show()
plot.write_html("combined.html")



