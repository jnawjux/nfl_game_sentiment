import pandas as pd
import got3 as got
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import inquirer

nfl_teams = {'Phoenix, AZ': 'Cardinals', 'Falcons': 'Atlanta, GA', 'Baltimore, MD': 'Ravens', 'Buffalo, NY': 'Bills',
'Charlotte, NC':'Panthers', 'Chicago, IL': 'Bears', 'Cincinnati, OH': 'Bengals', 'Cleveland, OH': 'Browns',
'Dallas, TX' : 'Cowboys', 'Denver, CO': 'Broncos', 'Detroit, MI': 'Lions', 'Green Bay, WI': 'Packers',
'Houston, TX': 'Texans', 'Indianapolis, IN': 'Colts', 'Jacksonville, FL': 'Jaguars', 'Kansas City, MO': 'Chiefs',
'Los Angeles, CA': 'Chargers', 'Los Angeles, CA': 'Rams', 'Miami, FL': 'Dolphins', 'Minnesota': 'Vikings',
'Boston, MA': 'Patriots', 'New Orleans, LA': 'Saints', 'New York, NY': 'Giants', 'New York, NY': 'Jets',
'Oakland, CA': 'Raiders', 'Philadelphia, PA': 'Eagles', 'Pittsburgh, PA': 'Steelers', 'San Francisco, CA': '49ers',
'Seattle, WA': 'Seahawks', 'Tampa Bay, FL': 'Buccaneers', 'Nashville, TN': 'Titans', 'Washington, D.C.': 'Redskins'}

team = [
  inquirer.List('team',
                message="Which team do you want sentiment stats for?",
                choices=nfl_teams.values(),
            ),
]
team_selection = inquirer.prompt(team)
start_date = input("What start date? (eg. format 01-30-2019)")
end_date = input("What end date? (eg. format 01-30-2019)")

def get_tweets(start_date, end_date, team_name, location):
    """
    Return tweets for an individual day, based on search criteria
    """
    tweetCriteria = got.manager.TweetCriteria()\
                   .setQuerySearch(team_name)\
                   .setSince(start_date)\
                   .setUntil(end_date)\
                   .setWithin(location)\
                   .setTopTweets(True)\
                   .setMaxTweets(25)
 
    return got.manager.TweetManager.getTweets(tweetCriteria)

def get_sentiment(tweets):
    """
    Return percentage pos / neg tweets for individual day
    """
    analyzer = SentimentIntensityAnalyzer()
    total_score = {'Positive': 0, 'Negative': 0}
    for tweet in tweets:
        score = analyzer.polarity_scores(tweet.text)['compound']
        if score >= .05:
            total_score['Positive'] += 1
        elif score <= -0.05:
            total_score['Negative'] += 1 
    return (round((total_score['Positive']/sum(total_score.values())) * 100, 2), 
           round((total_score['Negative']/sum(total_score.values())) * 100, 2))

def create_csv()