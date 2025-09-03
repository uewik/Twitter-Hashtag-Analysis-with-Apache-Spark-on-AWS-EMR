from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col, concat_ws, regexp_extract

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Hashtag Word Analysis") \
    .getOrCreate()

# Read JSON file
# df = spark.read.json("tinyTwitter.json")
# df = spark.read.json("smallTwitter.json")
df = spark.read.json("s3://p2-inputdata/smallTwitter.json")

# Concatenate 'text' from 'doc' and 'description' from 'doc.user' and 'text' from 'value.properties'
concatenated_df = df.select(concat_ws(" ",
                                      col("doc.text"),
                                      col("doc.user.description"),
                                      col("value.properties.text"),
                                      )
                            .alias("combined_text"))

# Split the concatenated text into words
words_df = concatenated_df.select(explode(split(lower(col("combined_text")), "\s+")).alias("word"))

# Filter words that start with '#'
hashtags_df = words_df.select(regexp_extract(col("word"), r"(#\w+)", 1).alias("hashtag"))


clean_hashtags_df = hashtags_df.filter(col("hashtag") != "")

# Count hashtag occurrences and sort them in descending order
top_hashtags = clean_hashtags_df.groupBy("hashtag") \
    .count() \
    .orderBy(col("count").desc()) \
    .limit(20)

# Show top 20 hashtags
top_hashtags.show()

# top_hashtags.toPandas().to_csv("output.csv", header=True, index=False)
output_path = "s3://cloudcomputingvt/Hao/output"
top_hashtags.coalesce(1).write.option("header", "true").csv(output_path)

# Stop Spark session
spark.stop()