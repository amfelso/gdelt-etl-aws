import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

"""
This Glue script transforms raw GDELT data in S3 by removing unwanted fields, renaming/typing fields for the output table,
joining with RDS dimensions and then loading to Redshift for analysis.
"""

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Load DynamicFrames from Glue Data Catalog
rawEvents = glueContext.create_dynamic_frame.from_catalog(
    database="gdelt-raw",
    table_name="gdelt",
    transformation_ctx="datasource0",
)
countryCodes = glueContext.create_dynamic_frame.from_catalog(
    database="gdelt-dimensions", table_name="dim_country"
)
eventCodes = glueContext.create_dynamic_frame.from_catalog(
    database="gdelt-dimensions", table_name="dim_event"
)

# Drop fields and map others to match output schema
# For more info on GDELT 2.0 Events fields, see here: http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf 
finalEvents = (rawEvents.drop_fields(["col1","col2","col4","col5","col6","col7","col8","col9","col10","col11",
                                    "col12","col13","col14","col15","col16","col17","col18","col19","col20","col21",
                                    "col22","col23","col24","col25","col27","col32","col33","col35","col36","col37",
                                    "col38","col39","col40","col41","col42","col43","col44","col45","col46","col47",
                                    "col48","col49","col50","col51","col52","col54","col55","col56","col57","col58",
                                    "col59"])
                        .apply_mapping([
                            ("col0", "long", "EventID", "int"),
                            ("col3", "long", "EventYear", "int"),
                            ("col26", "long", "EventSubtypeCode", "string"),
                            ("col28", "long", "EventTypeCode", "string"),
                            ("col29", "long", "QuadClass", "int"),
                            ("col30", "double", "GoldsteinScale", "double"),
                            ("col31", "long", "NumMentions", "int"),
                            ("col34", "double", "AvgTone", "double"),
                            ("col53", "string", "EventCountryCode", "string"),
                            ("col60", "string", "SourceURL", "string")
                        ])
)

# Join with country dimension 
finalEvents = (finalEvents.join(paths1=["EventCountryCode"], paths2=["CODE"], frame2=countryCodes)
                          .rename_field("LABEL","EventCountry")
                          .drop_fields(["EventCountryCode","CODE"])
)

# Joins with event dimension 
finalEvents = (finalEvents.join(paths1=["EventTypeCode"], paths2=["CAMEOEVENTCODE"], frame2=eventCodes)
                          .rename_field("EVENTDESCRIPTION","EventType")
                          .drop_fields(["EventTypeCode","CAMEOEVENTCODE"])
)
finalEvents = (finalEvents.join(paths1=["EventSubtypeCode"], paths2=["CAMEOEVENTCODE"], frame2=eventCodes)
                          .rename_field("EVENTDESCRIPTION","EventSubtype")
                          .drop_fields(["EventSubtypeCode","CAMEOEVENTCODE"])
)

# Load frame to Redshift
redshiftCluster = glueContext.write_dynamic_frame.from_catalog(
    frame=finalEvents,
    database="gdelt-reporting",
    table_name="dev_public_eventsbycountryandtype",
    redshift_tmp_dir=args["TempDir"],
    transformation_ctx="redshiftCluster"
)

job.commit()
