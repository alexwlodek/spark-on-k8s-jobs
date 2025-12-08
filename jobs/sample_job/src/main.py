from pyspark.sql import SparkSession

def main():
    spark = (SparkSession.builder
             .appName("sample-job")
             .getOrCreate())

    # Tu docelowo czytasz z S3
    df = spark.range(0, 100)
    result = df.groupBy().sum("id").collect()[0][0]

    print(f"Result = {result}")

    # Tu docelowo zapis do S3
    # df.write.mode("overwrite").parquet("s3a://your-bucket/path")

    spark.stop()

if __name__ == "__main__":
    main()
