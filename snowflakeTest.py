import snowflake.connector

SqlStmt2 = """
        SELECT DISTINCT FieldName 
          FROM Tables3VX 
         WHERE DatabaseName = 'CMS_VDM_VIEW_MDCR_PRD' 
           AND TableName = 'V2_MDCR_CLM' ; 
        """

##########################################
# MySQL Connection string values
##########################################
snowflake_user="idrc_dev_bia_ptb_etl"
snowflake_password="Df$kLwR341"
snowflake_account="cms-idrnp.privatelink"
#snowflake_account="cms-idrnp"
snowflake_warehouse="idrc_dev_transform_wh"
snowflake_database="idrc_dev"
snowflake_host="cms-idrnp.privatelink.snowflakecomputing.com:443"
#snowflake_host="http://ocsp.cms-idrnp.privatelink.snowflakecomputing.com"

"""
    {"SNOW_USER": "idrc_dev_bia_ptb_etl",
    "SNOW_PASSWORD": "Df$kLwR341",
    "SNOW_ACCOUNT": "cms-idrnp.privatelink",
    "SNOW_DATABASE": "idrc_dev",
    "SNOW_WAREHOUSE": "idrc_dev_transform_wh",
    "SNOW_TIMEOUT": "30"}

cnx = snowflake.connector.Connect(user={my_userid}, password={my_password}, 
    host="https://cms-impl.okta.com/",
    account="cms-idrnp",
    warehouse="BIA_NP_ETL_WKLD",
    database="IDRC_DEV",
    schema="CMS_DIM_GEO_DEV"
)
"""

"""
snowflake_user="BZH3"
snowflake_password="trbr0r0R" 
snowflake_account="cms-idrnp.privatelink"
snowflake_warehouse="BIA_NP_ETL_WKLD"
snowflake_database="IDRC_DEV"
#snowflake_database="SNOWFLAKE_SAMPLE_DATA"
snowflake_schema="CMS_DIM_GEO_DEV"
#snowflake_schema="INFORMATION_SCHEMA"
snowflake_host="https://cms-impl.okta.com/"
#snowflake_host="https://impl.idp.idm.cms.gov/"
"""

###############################
# Extract configuration values
###############################
try: 

    ###################################################
    # Connect to MySQL
    ###################################################   
    # ConnectionString="account={YOUR_ACCOUNT_ID};host={YOUR_HOST};user={YOUR_USERNAME};password={YOUR_PASSWORD};db=SNOWFLAKE_SAMPLE_DATA;"
    #   
    cnx = snowflake.connector.Connect(user=snowflake_user, password=snowflake_password, 
        host=snowflake_host,
        account=snowflake_account,
        authenticator='externalbrowser',
        warehouse=snowflake_warehouse,
        database=snowflake_database
        ,schema=None
        #,schema=snowflake_schema
        
    )

    
    print("Connected to Snowflake!")

except Exception as ex:
    print("Could not connect to Snowflake!")
    print(ex)



