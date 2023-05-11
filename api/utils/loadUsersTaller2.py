

import json
import os
import numpy as np
import pandas as pd
import requests

import pyspark.sql.functions as F
# from nltk.corpus import stopwords
from pyspark import SparkConf
from pyspark.ml import *
from pyspark.ml import Pipeline
from pyspark.ml.feature import *
from pyspark.sql import Row, SparkSession
from pyspark.sql import Window
from pyspark.sql import functions as F
from pyspark.sql.functions import (
    col,
    desc,
    expr,
    first,
    length,
    lit,
    regexp_replace,
    row_number,
    split,
    substring,
    to_date,
    to_timestamp,
    when,
    explode, collect_list
)
from pyspark.sql.types import *
# from wordcloud import WordCloud
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import HashingTF, IDF, CountVectorizer, StopWordsRemover
from pyspark.ml.clustering import BisectingKMeans
from pyspark.ml.functions import vector_to_array
from pyspark.ml.clustering import LDA
from flask import Response
# add 992 unique users to the db

# spark = SparkSession.builder.config("spark.driver.memory", "15g").config("spark.executor.memory", "15g")\
#     .config("spark.driver.extraJavaOptions", "-Xss4M").config("spark.driver.extraClassPath", "postgresql-42.5.3.jar")\
#     .master("local[*]").getOrCreate()

# persited_predictions_df = spark.read.parquet(
#     "persited_predictions_df.parquet").select(col("user_id_numeric").alias("username"))

# users = persited_predictions_df.withColumn(
#     "password", col("username"))
# users.show()
# (
#     users.write
#     .format("jdbc")
#     .option("url", "jdbc:postgresql://localhost/SDR")
#     .option("dbtable", "sdr.\"user\"")
#     .option("user", "postgres")
#     .option("password", "2006iaso")
#     .option("driver", "org.postgresql.Driver")
#     .option("truncate", True)
#     .mode("append")
#     .save()
# )

users = pd.read_parquet('persited_predictions_df.parquet')
print(users.head())
users_filtered = users.user_id_numeric.unique()  # [:2]
df = pd.DataFrame(users_filtered, columns=["user"])
print(df.head())

# df['json'] = df.rename(columns={"userid"
# df = pd.DataFrame(users_filtered, columns=["user"])
df["password"] = df["user"]
df = df.astype('int')
print(df.head())
# df = df.user.astype('int')
# df2 = df.password.astype('int').copy()
# df['json'] = df.rename(columns={"userid": "username"}).apply(
#     lambda x: x.to_json(), axis=1)

print(df.astype('int').dtypes)
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


all_rows = len(df)
for i in range(all_rows):

    row_dict = dict(df.iloc[i])

    row_dict = json.dumps(row_dict)
    print(row_dict)
    # callUserApi(row_dict)
