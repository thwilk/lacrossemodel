import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime

base_url = 'https://www.ncaa.com/stats/lacrosse-men/d1/current/team/538'
pages = ['p1', 'p2']  # Page identifiers
#colNames = ['Name', 'Team', 'Saves', 'Goals Allowed', 'Pct.']



def getStats(base_url):
    try:
        print("okay!")
        r = requests.get(base_url)
        print(r.status_code)
        with open("html.txt", "w") as f:
            f.write(str(r.text))

        soup = BeautifulSoup(r.text, 'html.parser')
        stats_table = soup.find("table")
        headers = [header.text.strip() for header in stats_table.find_all('th')]

        rows = []
        for row in stats_table.find_all('tr')[1:]:  # skip the header row
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                rows.append(cols)
        
        return headers, rows

    except requests.HTTPError as e:
        print(f'HTTP Error occurred: {e.response.status_code}')
        return None, None
    except requests.RequestException as e:
        print(f'Request exception: {e}')
        return None, None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None, None

# Initialize an empty list to collect all the data
all_rows = []
all_headers = None

# Loop through each page and scrape the data
for page in pages:
    url = base_url + "/"+page
    headers, rows = getStats(url)
    
    if headers and rows:
        all_headers = headers  # Save headers once
        all_rows.extend(rows)  # Collect rows from all pages

if all_headers and all_rows:
    # Create a DataFrame from the concatenated data
    df = pd.DataFrame(all_rows, columns=all_headers)
    
    # Save the DataFrame to a CSV file
    x = datetime.datetime.now().strftime("%x").replace("/","_")
    df.to_csv(f'template{x}.csv', index=False)
    print("Data saved to template.csv")
    