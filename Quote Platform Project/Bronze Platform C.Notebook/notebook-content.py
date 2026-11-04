# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "8adcea99-5f6c-4c24-92cd-a7f2742d5955",
# META       "default_lakehouse_name": "Bronze_LH",
# META       "default_lakehouse_workspace_id": "af8654ea-6e65-4a3a-95a1-fcfb5f99f885",
# META       "known_lakehouses": [
# META         {
# META           "id": "8adcea99-5f6c-4c24-92cd-a7f2742d5955"
# META         },
# META         {
# META           "id": "eecd10a4-6028-47b4-b6ae-8b4b4baf9917"
# META         }
# META       ]
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# CELL ********************

import pandas as pd

df_platform_c = pd.read_excel("/lakehouse/default/Files/Quotes/PlatformC/platform_c_quotes.xlsx",sheet_name="Quotes")

df_platform_c = spark.createDataFrame(df_platform_c)
df_platform_c.createOrReplaceTempView("platform_c_raw")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT COUNT(*) AS RowCount
# MAGIC FROM platform_c_raw;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM platform_c_raw
# MAGIC LIMIT 20;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC Product,
# MAGIC Stage,
# MAGIC COUNT(*) AS QuoteCount
# MAGIC FROM platform_c_raw
# MAGIC GROUP BY Product, Stage
# MAGIC ORDER BY Product, Stage;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_c_clean AS
# MAGIC 
# MAGIC SELECT
# MAGIC Reference AS QuoteID,
# MAGIC CAST(`Date Raised` AS DATE) AS QuoteDate,
# MAGIC Account AS CustomerName,
# MAGIC Office AS Branch,
# MAGIC `Sales Person` AS QuoteOwner,
# MAGIC `From` AS OriginUNLOCODE,
# MAGIC `To` AS DestinationUNLOCODE,
# MAGIC CASE
# MAGIC     WHEN Product IN ('FCL','LCL') THEN 'Sea'
# MAGIC     WHEN Product = 'AIR' THEN 'Air'
# MAGIC     WHEN Product = 'ROAD' THEN 'Road'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS TransportMode,
# MAGIC Curr AS Currency,
# MAGIC CAST(`Buy Price` AS DOUBLE) AS QuotedCostLocal,
# MAGIC CAST(`Sell Price` AS DOUBLE) AS QuotedSellLocal,
# MAGIC CASE
# MAGIC     WHEN Stage = 'Successful' THEN 'Won'
# MAGIC     WHEN Stage = 'Unsuccessful' THEN 'Lost'
# MAGIC     WHEN Stage = 'Pending' THEN 'Open'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS QuoteStatus,
# MAGIC Reason AS LostReason,
# MAGIC 'Platform C' AS SourcePlatform
# MAGIC FROM platform_c_raw;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM platform_c_clean
# MAGIC LIMIT 20;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC QuoteID,
# MAGIC COUNT(*) AS QuoteCount
# MAGIC FROM platform_c_clean
# MAGIC GROUP BY QuoteID
# MAGIC HAVING COUNT(*) > 1
# MAGIC ORDER BY QuoteCount DESC;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_c_dedup AS
# MAGIC 
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC     SELECT *,
# MAGIC     ROW_NUMBER() OVER( PARTITION BY QuoteID ORDER BY QuoteID) AS RowNumber
# MAGIC     FROM platform_c_clean
# MAGIC )
# MAGIC WHERE RowNumber = 1;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_c_valid AS
# MAGIC 
# MAGIC SELECT *
# MAGIC FROM platform_c_dedup
# MAGIC WHERE QuoteID IS NOT NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customer_mapping = (spark.read.option("header", "true").option("inferSchema", "true").csv("Files/Quotes/Dimensions/customer_mapping.csv"))

df_customer_mapping.createOrReplaceTempView("customer_mapping")

df_customer_mapping = (spark.read.option("header", "true").option("inferSchema", "true").csv("Files/Quotes/Dimensions/location_mapping.csv"))

df_customer_mapping.createOrReplaceTempView("location_mapping")   

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_c_final AS
# MAGIC 
# MAGIC SELECT
# MAGIC c.QuoteID,
# MAGIC c.QuoteDate,
# MAGIC m.Customer_ID AS CustomerID,
# MAGIC c.CustomerName,
# MAGIC c.Branch,
# MAGIC CAST(NULL AS STRING) AS Department,
# MAGIC c.QuoteOwner,
# MAGIC o.UNLOCODE AS OriginUNLOCODE,
# MAGIC d.UNLOCODE AS DestinationUNLOCODE,
# MAGIC c.TransportMode,
# MAGIC c.Currency,
# MAGIC c.QuotedCostLocal,
# MAGIC c.QuotedSellLocal,
# MAGIC c.QuoteStatus,
# MAGIC c.LostReason,
# MAGIC Cast(NULL AS DATE) AS LastUpdated,
# MAGIC c.SourcePlatform
# MAGIC FROM platform_c_valid c
# MAGIC LEFT JOIN customer_mapping m ON c.CustomerName = m.Source_Customer_Name AND m.Source_System = 'PlatformC'
# MAGIC LEFT JOIN location_mapping o ON c.OriginUNLOCODE = o.Source_Location
# MAGIC LEFT JOIN location_mapping d ON c.DestinationUNLOCODE = d.Source_Location;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC COUNT(*) AS TotalRows,
# MAGIC SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) AS MissingCustomers,
# MAGIC SUM(CASE WHEN OriginUNLOCODE IS NULL THEN 1 ELSE 0 END) AS MissingOrigins,
# MAGIC SUM(CASE WHEN DestinationUNLOCODE IS NULL THEN 1 ELSE 0 END) AS MissingDestinations
# MAGIC FROM platform_c_final;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Silver_LH.dbo.platform_c_quotes
# MAGIC USING DELTA AS
# MAGIC SELECT
# MAGIC QuoteID,
# MAGIC QuoteDate,
# MAGIC CustomerID,
# MAGIC CustomerName,
# MAGIC Branch,
# MAGIC CAST(Department AS STRING) AS Department,
# MAGIC QuoteOwner,
# MAGIC OriginUNLOCODE,
# MAGIC DestinationUNLOCODE,
# MAGIC TransportMode,
# MAGIC Currency,
# MAGIC CAST(QuotedCostLocal AS DOUBLE) AS QuotedCostLocal,
# MAGIC CAST(QuotedSellLocal AS DOUBLE) AS QuotedSellLocal,
# MAGIC QuoteStatus,
# MAGIC LostReason,
# MAGIC CAST(LastUpdated AS DATE) AS LastUpdated,
# MAGIC SourcePlatform
# MAGIC FROM platform_c_final;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
