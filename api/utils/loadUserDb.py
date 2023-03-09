

import json
import os
import numpy as np
import pandas as pd
import requests
# add 992 unique users to the db
users = pd.read_csv('./preprocessed_user_item_rating.csv')

users_filtered = users.userid.unique()  # [:2]
df = pd.DataFrame(users_filtered, columns=['username'])
df['password'] = df['username']
# df['json'] = df.rename(columns={"userid": "username"}).apply(
#     lambda x: x.to_json(), axis=1)


# print(users.userid.nunique())
CREATE_USERS_URL = "http://localhost:5000/api/auth/signIn"


def callApi(row):
    headers = {
        'content-type': "application/json"
    }

    response = requests.request(
        "POST", url=CREATE_USERS_URL, data=row, headers=headers)
    res = json.loads(response.content)
    print(res)


all_rows = len(df)
for i in range(all_rows):
    # choose the first half of cols before "activities"
    row_dict = dict(df.iloc[i])
    # add the "activites" with the rest of the cols
    # dict has single quotes which throws an error if sent to an API, so use json.dumps
    row_dict = json.dumps(row_dict)
    print(row_dict)
    callApi(row_dict)
