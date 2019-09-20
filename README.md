# NFL Team Sentiment analysis
This is a basic implimentation of [GetOldTweets](https://github.com/Jefferson-Henrique/GetOldTweets-python) and [vaderSentiment](https://github.com/cjhutto/vaderSentiment) to help gauge fan moral. When run, it returns a CSV file with the percentage postiive and negative for each day, based on 500 Top Tweets mentioning the team name, sent from the locality of the team (ex. Search for 500 Top Tweets for 'Browns' in Cleveland, OH).

To run:

```
python nfl_sentiment.py
```

You will then need to pick a team from the menu:

```
Which team do you want sentiment stats for?
> Cardinals
  Falcons
  Ravens
  Bills
  ...
```
Then select dates to and from:

```
What start date? (eg. format 2019-01-30):
What end date? (eg. format 2019-01-30):
```

Let run, and it will return a CSV file in the same directory named ```sentiment_stats.csv```

The CSV returns each row as a day, and defaults to searching for 500 tweets (can be adjusted, but do note more tweets will cause it to run longer).

Enjoy!
