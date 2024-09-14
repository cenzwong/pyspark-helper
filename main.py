import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from pysparky import cenz

from pysparky import functions_ext as F_
from pysparky import spark_ext as se
from pysparky import transformation_ext as te

print(pyspark.__version__)

spark = SparkSession.builder.getOrCreate()

spark.range(1).select(
    F_._lower(F.lit("HELLO")),
    F_.startswiths(F.lit("a12334"), ["123", "234"]),
    F.lit("HELLO")._lower(),
    F.lit("HELLO").startswiths(["hello", "HEL"]),
).show()

data_dict = {"key1": [1, 2, 3], "key2": [3]}
column_names = ["keys", "values"]
df = se.convert_dict_to_dataframe(spark, data_dict, column_names, explode=True)
df.show()
# key1,1
# key2,2

# pyspark.sql.SparkSession.convert_dict_to_dataframe = se.convert_dict_to_dataframe
spark.convert_dict_to_dataframe(data_dict, column_names, explode=True).show()

spark.range(1).select(F.lit("HELLO").chain(F.lower)).show()


spark.createDataFrame(
    [
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 2),
        (2, 3),
        (2, 4),
    ],
    ["key", "value"],
).get_latest_record_from_column("key", "value").show()
