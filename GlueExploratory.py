
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job



args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)



# Script generated for node idr-sf-connector
idrsfconnector_node1 = glueContext.create_dynamic_frame.from_options(
connection_type="custom.jdbc",
connection_options={
"tableName": "CMS_DIM_PTB_DEV.CLM_FMR_CARR",
"dbTable": "CMS_DIM_PTB_DEV.CLM_FMR_CARR",
"connectionName": "test-connector-snowflake",
},
transformation_ctx="idrsfconnector_node1",
)



# Script generated for node Amazon S3
AmazonS3_node1653334357007 = glueContext.write_dynamic_frame.from_options(
frame=idrsfconnector_node1,
connection_type="s3",
format="csv",
connection_options={
"path": "s3://aws-hhs-cms-eadg-bia-ddom-extracts/",
"partitionKeys": [],
},
transformation_ctx="AmazonS3_node1653334357007",
)



job.commit()