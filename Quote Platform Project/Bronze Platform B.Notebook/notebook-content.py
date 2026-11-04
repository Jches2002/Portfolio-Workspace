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

df_platform_b = (spark.read.option("multiline", "true").json("Files/Quotes/PlatformB/*.json"))

df_platform_b.createOrReplaceTempView("platform_b_raw")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT COUNT(*) AS RowCount
# MAGIC FROM platform_b_raw;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM platform_b_raw
# MAGIC LIMIT 20;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC service,
# MAGIC outcome,
# MAGIC COUNT(*) AS QuoteCount
# MAGIC FROM platform_b_raw
# MAGIC GROUP BY service, outcome
# MAGIC ORDER BY service, outcome;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_b_clean AS
# MAGIC 
# MAGIC SELECT
# MAGIC quoteNumber AS QuoteID,
# MAGIC CAST(createdAt AS DATE) AS QuoteDate,
# MAGIC account.reference AS CustomerID,
# MAGIC account.name AS CustomerName,
# MAGIC office AS Branch,
# MAGIC CAST(NULL AS STRING) AS Department,
# MAGIC owner AS QuoteOwner,
# MAGIC route.from AS OriginUNLOCODE,
# MAGIC route.to AS DestinationUNLOCODE,
# MAGIC CASE
# MAGIC     WHEN service = 'Ocean Freight' THEN 'Sea'
# MAGIC     WHEN service = 'Air Freight' THEN 'Air'
# MAGIC     WHEN service = 'Road Transport' THEN 'Road'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS TransportMode,
# MAGIC pricing.currency AS Currency,
# MAGIC pricing.buy AS QuotedCostLocal,
# MAGIC pricing.sell AS QuotedSellLocal,
# MAGIC CASE
# MAGIC     WHEN outcome = 'Converted' THEN 'Won'
# MAGIC     WHEN outcome = 'Unsuccessful' THEN 'Lost'
# MAGIC     WHEN outcome = 'In Progress' THEN 'Open'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS QuoteStatus,
# MAGIC failureReason AS LostReason,
# MAGIC CAST(updatedAt AS TIMESTAMP) AS LastUpdated,
# MAGIC 'Platform B' AS SourcePlatform
# MAGIC FROM platform_b_raw;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC Select * from platform_b_clean

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM platform_b_clean
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
# MAGIC FROM platform_b_clean
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
# MAGIC CREATE OR REPLACE TEMP VIEW platform_b_dedup AS
# MAGIC 
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC     SELECT *,
# MAGIC     ROW_NUMBER() OVER(
# MAGIC         PARTITION BY QuoteID
# MAGIC         ORDER BY LastUpdated DESC
# MAGIC     ) AS RowNumber
# MAGIC     FROM platform_b_clean
# MAGIC )
# MAGIC WHERE RowNumber = 1;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_b_valid AS
# MAGIC 
# MAGIC SELECT *
# MAGIC FROM platform_b_dedup
# MAGIC WHERE QuoteID IS NOT NULL;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC COUNT(*) AS ValidRows,
# MAGIC COUNT(DISTINCT QuoteID) AS UniqueQuotes
# MAGIC FROM platform_b_valid;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_location_mapping = ( spark.read.option("header", "true").option("inferSchema", "true") .csv("Files/Quotes/Dimensions/location_mapping.csv"))

df_location_mapping.createOrReplaceTempView("location_mapping")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM location_mapping
# MAGIC LIMIT 20;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMP VIEW platform_b_final AS
# MAGIC 
# MAGIC SELECT
# MAGIC b.QuoteID,
# MAGIC b.QuoteDate,
# MAGIC b.CustomerID,
# MAGIC b.CustomerName,
# MAGIC b.Branch,
# MAGIC CAST(NULL AS STRING) AS Department,
# MAGIC b.QuoteOwner,
# MAGIC o.UNLOCODE AS OriginUNLOCODE,
# MAGIC d.UNLOCODE AS DestinationUNLOCODE,
# MAGIC b.TransportMode,
# MAGIC b.Currency,
# MAGIC b.QuotedCostLocal,
# MAGIC b.QuotedSellLocal,
# MAGIC b.QuoteStatus,
# MAGIC b.LostReason,
# MAGIC b.LastUpdated,
# MAGIC b.SourcePlatform
# MAGIC FROM platform_b_valid b
# MAGIC LEFT JOIN location_mapping o ON b.OriginUNLOCODE = o.Source_Location
# MAGIC LEFT JOIN location_mapping d ON b.DestinationUNLOCODE = d.Source_Location;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM platform_b_final
# MAGIC LIMIT 20;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC COUNT(*) AS TotalRows,
# MAGIC SUM(CASE WHEN OriginUNLOCODE IS NULL THEN 1 ELSE 0 END) AS MissingOrigins,
# MAGIC SUM(CASE WHEN DestinationUNLOCODE IS NULL THEN 1 ELSE 0 END) AS MissingDestinations
# MAGIC FROM platform_b_final;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Silver_LH.dbo.platform_b_quotes
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT
# MAGIC QuoteID,
# MAGIC QuoteDate,
# MAGIC CustomerID,
# MAGIC CustomerName,
# MAGIC Branch,
# MAGIC CAST(NULL AS STRING) AS Department,
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
# MAGIC FROM platform_b_final;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM Portfolio.Silver_LH.dbo.platform_b_quotes
# MAGIC LIMIT 20;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
