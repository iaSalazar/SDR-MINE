import json
import os
import pickle
from flask_restful import Resource
import pandas as pd
from ..app.extensions import db, api, guard
from flask import request
from flask_restful import Resource
import flask_praetorian
from sklearn.neighbors import NearestNeighbors

import shutil
import time
# import nltk
import numpy as np
import pandas as pd
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


class ResourceSparkRecommenderALS(Resource):
    # TODO

    def get(self, userId):

        spark = SparkSession.builder.config("spark.driver.memory", "15g").config("spark.executor.memory", "15g")\
            .config("spark.driver.extraJavaOptions", "-Xss4M").master("local[*]").getOrCreate()

        persited_predictions_df = spark.read.parquet(
            "./utils/persited_predictions_df.parquet")

        df = persited_predictions_df.filter(col("user_id_numeric") == userId).withColumn('exploded_arr', explode('recommendations'))\
            .select("user_id_numeric", "exploded_arr", "exploded_arr.business_id_numeric", "exploded_arr.rating")

        answer = df.pandas_api().to_json(orient="records")

        return Response(answer, mimetype='application/json')


api.add_resource(ResourceSparkRecommenderALS,
                 '/api/sparkRecommenderALS/<int:userId>/')
