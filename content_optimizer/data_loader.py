import pandas as pd

def load_data():
    creators = pd.read_csv("creators.csv")
    activity = pd.read_csv("platform_activity.csv")
    history = pd.read_csv("historical_engagement.csv")
    content = pd.read_csv("content.csv")
    return creators, activity, history, content
