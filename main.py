import pandas as pd
import got3 as got
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import inquirer

nfl_teams = {'Cardinals': 'Phoenix, AZ',
            'Atlanta, GA': 'Falcons',
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
start_date = input("What start date? (eg. format 01-30-2019)")
end_date = input("What end date? (eg. format 01-30-2019)")
location = nfl_teams[team_selection]

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

def date_range(date1, date2):
    """
    """
    dt1 = datetime.strptime(date1, '%Y-%m-%d') 
    dt2 = datetime.strptime(date2, '%Y-%m-%d') 
    for n in range(int((dt2 - dt1).days) + 1):
        yield dt1 + timedelta(n)
        
def create_date_tuples(date1, date2):
    """
    """
    from_date = [dt.strftime("%Y-%m-%d") 
                    for dt in date_range(date1, date2)]

    to_date = [dt.strftime("%Y-%m-%d") 
                    for dt in date_range((datetime.strptime(date1, '%Y-%m-%d')\
                                        + timedelta(days=1)).strftime("%Y-%m-%d")
                                        ,(datetime.strptime(date2, '%Y-%m-%d')\
                                         + timedelta(days=1)).strftime("%Y-%m-%d"))]

    return list(zip(from_date, to_date))


