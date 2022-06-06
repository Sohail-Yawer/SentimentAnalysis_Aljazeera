# SentimentAnalysis_Aljazeera
Sentiment Analysis of ten latest articles of Aljazeera from mozambique 

Firstly, I collected 10 articles from the given URL.
This was done in two parts where a few articles contained featured list class in their div tag while others add a different tag.
Using bs4 tag series lists, I combined them and made them to a list of 10 articles.

The json file contains data with articles tag and has 10 datapoints with title and url attributes.

I iterated over the combined bs4 tag elements and extracted title and content from them. I cleaned the data on the go as well.
Then I added the data to a list so that it can be used to make a pandas DataFrame to calculate sentiment of the articles content

Now as the dataframe is ready I performed sentiment analysis on the content, firstly using textblob library of python which returns a polarity value. The values for polarity of the articles was very low( for example 0.02 etc)

Since the scores are very low(scale of polarity is between -1 and 1 where 1 indicates Positive and -1 indicates Negative, 0 is neutral)
I used another way to get the sentiment of articles which includes counting the number of positive and negative words and deciding based on those values the sentiment of the content

For this I used the Loughran-McDonald Master Dictionary from 1993 to 2021. This csv file is also included in the repo.
It contains words with sentiment categories pertaining to them.
The sentiment categories are: negative, positive, uncertainty, litigious, strong modal, weak modal, and constraining

Using this I counnted the number of positive and negative words in the content of an article.
I removed stopwords which wont affect the sentiment of the article.

If difference between number of positive and negative words is less than 1 then the sentiment is Neutral, if count of positive words is higher than negative then sentiment is Positive, else Negative

Lastly I used plotly to plot the classification of sentiment of the articles using scatterplot, histogram and a combined plot with a dropdown menu of both of them.

The total time elasped using tqdm library is 00:07

To run the code download the repo and firstly run pip install requirements.txt then make sure to include the Loughran-McDonald Master Dictionary from 1993 to 2021 csv file in the same directory as the SentimentAnalysis_Aljareeza.py file. After making sure of this just run the .py file, it will generate the interactive .html plotly visualisations.