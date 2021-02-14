Welcome to Duke's Strava API python app!

Make sure you generate a *.env file with the fillowing format:

```
client_id=*
client_secret=*
```

# Quick Start

```{python}
import strava
import pandas as pd

c = strava.client()
c.get_athlete()
df = c.get_activities()

# convert to datetime
    for col in [x for x in df.columns if 'date' in x]:
        df[col] = pd.to_datetime(df[col])
```

# Step-by-Step
## Step 1 Requesting Access
http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all
Once authorized, this will take you to error, page the newly minted authorization code is in the URL

## Step 2 - Initialize your python Strava app
Test making an API call using `client.get_activities()`.

# Token Scopes
| Scope              | Description |
| ------------------ | ----------- |
| 'read'             | 'read public segments, public routes, public profile data, public posts, public events, club feeds, and leaderboards' |
| 'read_all'         | 'read private routes, private segments, and private events for the user' |
| 'profile:read_all' | 'read all profile information even if the user has set their profile visibility to Followers or Only You' |
| 'profile:write'    | 'update the user\'s weight and Functional Threshold Power (FTP), and access to star or unstar segments on their behalf' |
| 'activity:read'    | 'read the user\'s activity data for activities that are visible to Everyone and Followers, excluding privacy zone data' |
| 'activity:read_all'| 'the same access as activity:read, plus privacy zone data and access to read the user\'s activities with visibility set to Only You' |
| 'activity:write'   | 'access to create manual activities and uploads, and access to edit any activities that are visible to the app, based on activity read access level'}) |

# Related Documentation
https://developers.strava.com/docs/getting-started/