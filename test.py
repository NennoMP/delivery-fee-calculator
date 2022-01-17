from datetime import datetime as dt
import os

os.environ['TZ'] = 'UTC'
test = "2022-01-17T15:15:00Z"

today = dt.today().strftime('%Y-%m-%dT%H:%M:%SZ')

print(test < today)