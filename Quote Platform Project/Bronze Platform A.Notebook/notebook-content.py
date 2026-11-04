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
# META     }
# META   }
# META }

# CELL ********************

df_platform_a = (spark.read.option("header", "true").option("inferSchema", "true").csv("Files/Quotes/PlatformA/*.csv"))

df_platform_a.createOrReplaceTempView("platform_a_raw")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC SELECT COUNT(*) AS RowCount
# MAGIC FROM platform_a_raw;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC Transport_Mode,
# MAGIC Quote_Status,
# MAGIC COUNT(*) AS QuoteCount
# MAGIC FROM platform_a_raw
# MAGIC GROUP BY
# MAGIC Transport_Mode, Quote_Status
# MAGIC ORDER BY
# MAGIC Transport_Mode, Quote_Status;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC COUNT(*) AS TotalRows,
# MAGIC SUM(CASE WHEN Quote_ID IS NULL OR TRIM(Quote_ID) = '' THEN 1 ELSE 0 END) AS MissingQuoteIDs,
# MAGIC SUM(CASE WHEN Customer_Code IS NULL OR TRIM(Customer_Code) = '' THEN 1 ELSE 0 END) AS MissingCustomerCodes,
# MAGIC SUM(CASE WHEN Quoted_Sell <= 0 THEN 1 ELSE 0 END) AS InvalidSellPrices,
# MAGIC SUM(CASE WHEN Quoted_Cost < 0 THEN 1 ELSE 0 END) AS NegativeCosts,
# MAGIC SUM(CASE WHEN Quote_Status = 'LOST' AND (Lost_Reason IS NULL OR TRIM(Lost_Reason) = '') THEN 1 ELSE 0 END) AS MissingLostReasons
# MAGIC FROM platform_a_raw;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC TRIM(Quote_ID) AS QuoteID,
# MAGIC CAST(Created_Date AS DATE) AS QuoteDate,
# MAGIC TRIM(Customer_Code) AS CustomerID,
# MAGIC TRIM(Customer_Name) AS CustomerName,
# MAGIC Branch,
# MAGIC Department,
# MAGIC Quote_Owner AS QuoteOwner,
# MAGIC Origin_UNLOCODE AS OriginUNLOCODE,
# MAGIC Destination_UNLOCODE AS DestinationUNLOCODE,
# MAGIC CASE
# MAGIC     WHEN Transport_Mode = 'SEA' THEN 'Sea'
# MAGIC     WHEN Transport_Mode = 'AIR' THEN 'Air'
# MAGIC     WHEN Transport_Mode = 'ROAD' THEN 'Road'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS TransportMode,
# MAGIC Currency,
# MAGIC Quoted_Cost AS QuotedCostLocal,
# MAGIC Quoted_Sell AS QuotedSellLocal,
# MAGIC CASE
# MAGIC     WHEN Quote_Status = 'WON' THEN 'Won'
# MAGIC     WHEN Quote_Status = 'LOST' THEN 'Lost'
# MAGIC     WHEN Quote_Status = 'OPEN' THEN 'Open'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS QuoteStatus,
# MAGIC TRIM(Lost_Reason) AS LostReason,
# MAGIC CAST(Last_Updated AS DATE) AS LastUpdated,
# MAGIC 'Platform A' AS SourcePlatform
# MAGIC FROM platform_a_raw;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_a_clean AS
# MAGIC SELECT
# MAGIC TRIM(Quote_ID) AS QuoteID,
# MAGIC CAST(Created_Date AS DATE) AS QuoteDate,
# MAGIC TRIM(Customer_Code) AS CustomerID,
# MAGIC TRIM(Customer_Name) AS CustomerName,
# MAGIC Branch,
# MAGIC Department,
# MAGIC Quote_Owner AS QuoteOwner,
# MAGIC Origin_UNLOCODE AS OriginUNLOCODE,
# MAGIC Destination_UNLOCODE AS DestinationUNLOCODE,
# MAGIC CASE
# MAGIC     WHEN Transport_Mode = 'SEA' THEN 'Sea'
# MAGIC     WHEN Transport_Mode = 'AIR' THEN 'Air'
# MAGIC     WHEN Transport_Mode = 'ROAD' THEN 'Road'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS TransportMode,
# MAGIC Currency,
# MAGIC Quoted_Cost AS QuotedCostLocal,
# MAGIC Quoted_Sell AS QuotedSellLocal,
# MAGIC CASE
# MAGIC     WHEN Quote_Status = 'WON' THEN 'Won'
# MAGIC     WHEN Quote_Status = 'LOST' THEN 'Lost'
# MAGIC     WHEN Quote_Status = 'OPEN' THEN 'Open'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS QuoteStatus,
# MAGIC TRIM(Lost_Reason) AS LostReason,
# MAGIC CAST(Last_Updated AS DATE) AS LastUpdated,
# MAGIC 'Platform A' AS SourcePlatform
# MAGIC FROM platform_a_raw;

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
# MAGIC FROM platform_a_clean
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
# MAGIC CREATE OR REPLACE TEMP VIEW platform_a_dedup AS
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC     SELECT *,
# MAGIC     ROW_NUMBER() OVER( PARTITION BY QuoteID ORDER BY LastUpdated DESC ) AS RowNumber FROM platform_a_clean)
# MAGIC WHERE RowNumber = 1;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC COUNT(*) AS RowCount,
# MAGIC COUNT(DISTINCT QuoteID) AS UniqueQuotes
# MAGIC FROM platform_a_dedup;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_a_bronze_final AS
# MAGIC SELECT *
# MAGIC FROM platform_a_dedup
# MAGIC WHERE QuoteID IS NOT NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Silver_LH.dbo.platform_a_quotes
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT
# MAGIC QuoteID,
# MAGIC QuoteDate,
# MAGIC CustomerID,
# MAGIC CustomerName,
# MAGIC Branch,
# MAGIC Department,
# MAGIC QuoteOwner,
# MAGIC OriginUNLOCODE,
# MAGIC DestinationUNLOCODE,
# MAGIC TransportMode,
# MAGIC Currency,
# MAGIC QuotedCostLocal,
# MAGIC QuotedSellLocal,
# MAGIC QuoteStatus,
# MAGIC LostReason,
# MAGIC LastUpdated,
# MAGIC SourcePlatform
# MAGIC FROM platform_a_bronze_final;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
