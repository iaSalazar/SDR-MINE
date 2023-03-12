

import json
import os
import numpy as np
import pandas as pd
import requests
# add 992 unique users to the db
users = pd.read_csv('./preprocessed_user_item_rating.csv')
artists = pd.read_csv('./item-item-matrix.csv')['artist-name'].tolist()
users_filtered = users.userid.unique()  # [:2]
df = pd.DataFrame(users_filtered, columns=['username'])
df['password'] = df['username']
# df['json'] = df.rename(columns={"userid": "username"}).apply(
#     lambda x: x.to_json(), axis=1)


# print(users.userid.nunique())
CREATE_USERS_URL = "http://localhost:5000/api/auth/signIn"

CREATE_ARTIST_URL = "http://localhost:5000/api/artists"


def callUserApi(row):
    headers = {
        'content-type': "application/json"
    }

    response = requests.request(
        "POST", url=CREATE_USERS_URL, data=row, headers=headers)
    res = json.loads(response.content)
    print(res)


def callArtistApi(row):
    headers = {
        'content-type': "application/json"
    }

    response = requests.request(
        "POST", url=CREATE_ARTIST_URL, data=row, headers=headers)
    res = json.loads(response.content)
    print(res)


all_rows = len(df)
for i in range(all_rows):

    row_dict = dict(df.iloc[i])

    row_dict = json.dumps(row_dict)
    print(row_dict)
    callUserApi(row_dict)

for artist in artists:
    row_dict = {"name": artist}
    print(artist)

    row_dict = json.dumps(row_dict)
    print(row_dict)
    callArtistApi(row_dict)
