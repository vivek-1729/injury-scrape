import requests
import pandas as pd
from os.path import isfile

# URL of the website
urls = ["https://hashtagbasketball.com/injury/nba-health-and-safety-protocols", "https://hashtagbasketball.com/injury/illness", "https://hashtagbasketball.com/injury/sprained-left-ankle", "https://hashtagbasketball.com/injury/sprained-right-ankle", "https://hashtagbasketball.com/injury/sore-left-knee", "https://hashtagbasketball.com/injury/sore-right-knee", "https://hashtagbasketball.com/injury/concussion", "https://hashtagbasketball.com/injury/sore-left-ankle", "https://hashtagbasketball.com/injury/sore-lower-back", "https://hashtagbasketball.com/injury/left-knee-injury"]
#Already scraped the urls above. TODO: Need to input a new list of urls and run the program

def scrape_data(url):
    if(isfile("data.csv")): #Check if the data.csv already exists
        old_df = pd.read_csv("data.csv") #if it exists, we will append onto it
    else:
        old_df = None #if it doesn't exist, we'll create a new one

    response = requests.get(url)
    injury = url.split('/')[-1].replace('-', ' ')    

    if response.status_code == 200:
        df = pd.read_html(response.text)[0]
        df = df[~df["PLAYER"].str.contains("PLAYER", na=False)] #clean up their formatitng
        df["INJURY TYPE"] = injury #add a column for the injury
        if old_df is None:
            df.to_csv("data.csv", index=False)
        else:
            combined = pd.concat([old_df, df])
            combined.to_csv("data.csv", index=False)
    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")
        return 1
    return 0

list(map(scrape_data, urls))