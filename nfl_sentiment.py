import pandas as pd
import got3 as got
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import inquirer

nfl_teams = {'Cardinals': 'Phoenix, AZ',
            'Falcons': 'Atlanta, GA',
            'Ravens': 'Baltimore, MD',
            'Bills': 'Buffalo, NY',
            'Panthers': 'Charlotte, NC',
            'Bears': 'Chicago, IL',
            'Bengals': 'Cincinnati, OH',
            'Browns': 'Cleveland, OH',
            'Cowboys': 'Dallas, TX',
            'Broncos': 'Denver, CO',
            'Lions': 'Detroit, MI',
            'Packers': 'Green Bay, WI',
            'Texans': 'Houston, TX',
            'Colts': 'Indianapolis, IN',
            'Jaguars': 'Jacksonville, FL',
            'Chiefs': 'Kansas City, MO',
            'Rams': 'Los Angeles, CA',
            'Dolphins': 'Miami, FL',
            'Vikings': 'Minnesota',
            'Patriots': 'Boston, MA',
            'Saints': 'New Orleans, LA',
            'Jets': 'New York, NY',
            'Raiders': 'Oakland, CA',
            'Eagles': 'Philadelphia, PA',
            'Steelers': 'Pittsburgh, PA',
            '49ers': 'San Francisco, CA',
            'Seahawks': 'Seattle, WA',
            'Buccaneers': 'Tampa Bay, FL',
            'Titans': 'Nashville, TN',
            'Redskins': 'Washington, D.C.'}

team = [
  inquirer.List('team',
                message="Which team do you want sentiment stats for?",
                choices=nfl_teams.keys(),
            ),
]
team_selection = inquirer.prompt(team)
start_date = input("What start date? (eg. format 2019-01-30):  ")
end_date = input("What end date? (eg. format 2019-02-30):  ")
team_choice = team_selection['team']
location = nfl_teams[team_choice]

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
                   .setMaxTweets(500)
 
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

def date_range(date1, date2):
    """
    Return all the dates between two given dates
    """
    dt1 = datetime.strptime(date1, '%Y-%m-%d') 
    dt2 = datetime.strptime(date2, '%Y-%m-%d') 
    for n in range(int((dt2 - dt1).days) + 1):
        yield dt1 + timedelta(n)
        
def create_date_tuples(date1, date2):
    """
    Return list of tuples with start and end dates
    """
    from_date = [dt.strftime("%Y-%m-%d") 
                    for dt in date_range(date1, date2)]

    to_date = [dt.strftime("%Y-%m-%d") 
                    for dt in date_range((datetime.strptime(date1, '%Y-%m-%d')\
                                        + timedelta(days=1)).strftime("%Y-%m-%d")
                                        ,(datetime.strptime(date2, '%Y-%m-%d')\
                                         + timedelta(days=1)).strftime("%Y-%m-%d"))]

    return list(zip(from_date, to_date))

def create_csv(start_date, end_date, team_name, location):
    """
    Create and export sentiment data to CSV
    """
    file = open('sentiment_stats.csv','w')
    file.write('date,pos,neg\n')
    date_range_list = create_date_tuples(start_date, end_date)
    for day in date_range_list:
        day_tweets = get_tweets(day[0], day[1], team_name, location)
        day_sentiment = get_sentiment(day_tweets)
        file.write(f"{day[0]},{day_sentiment[0]},{day_sentiment[1]}")
        file.write('\n')
    file.close()

create_csv(start_date, end_date, team_choice, location)