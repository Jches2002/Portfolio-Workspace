# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "eecd10a4-6028-47b4-b6ae-8b4b4baf9917",
# META       "default_lakehouse_name": "Silver_LH",
# META       "default_lakehouse_workspace_id": "af8654ea-6e65-4a3a-95a1-fcfb5f99f885",
# META       "known_lakehouses": [
# META         {
# META           "id": "808cf73d-b495-4ed5-832e-60052054b64a"
# META         },
# META         {
# META           "id": "eecd10a4-6028-47b4-b6ae-8b4b4baf9917"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM dbo.quotes_gbp
# MAGIC LIMIT 10;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.DimCustomer
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC CustomerID,
# MAGIC CustomerName
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE CustomerID IS NOT NULL;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM Portfolio.Gold_LH.dbo.DimCustomer
# MAGIC ORDER BY CustomerID;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.DimBranch
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC Branch
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE Branch IS NOT NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM Portfolio.Gold_LH.dbo.DimBranch
# MAGIC ORDER BY Branch;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.DimPlatform
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC SourcePlatform
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE SourcePlatform IS NOT NULL;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.DimTransportMode
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC TransportMode
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE TransportMode IS NOT NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.DimQuoteStatus
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC QuoteStatus
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE QuoteStatus IS NOT NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.DimEmployee
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC QuoteOwner
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE QuoteOwner IS NOT NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.DimLostReason
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC LostReason
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE LostReason IS NOT NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.DimLocation
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC OriginUNLOCODE AS UNLOCODE
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE OriginUNLOCODE IS NOT NULL
# MAGIC 
# MAGIC UNION
# MAGIC 
# MAGIC SELECT DISTINCT
# MAGIC DestinationUNLOCODE AS UNLOCODE
# MAGIC FROM dbo.quotes_gbp
# MAGIC WHERE DestinationUNLOCODE IS NOT NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE Portfolio.Gold_LH.dbo.FactQuote
# MAGIC USING DELTA AS
# MAGIC 
# MAGIC SELECT
# MAGIC QuoteID,
# MAGIC QuoteDate,
# MAGIC CustomerID,
# MAGIC Branch,
# MAGIC QuoteOwner,
# MAGIC OriginUNLOCODE,
# MAGIC DestinationUNLOCODE,
# MAGIC SourcePlatform,
# MAGIC TransportMode,
# MAGIC QuoteStatus,
# MAGIC LostReason,
# MAGIC Currency,
# MAGIC QuotedCostLocal,
# MAGIC QuotedSellLocal,
# MAGIC ExchangeRate,
# MAGIC QuotedCostGBP,
# MAGIC QuotedSellGBP,
# MAGIC GrossProfitGBP,
# MAGIC GrossProfitMargin
# MAGIC FROM dbo.quotes_gbp;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *
# MAGIC FROM Portfolio.Gold_LH.dbo.FactQuote
# MAGIC LIMIT 20;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT COUNT(*) AS QuoteCount
# MAGIC FROM Portfolio.Gold_LH.dbo.FactQuote;
# MAGIC 
# MAGIC SELECT COUNT(*) AS QuoteCount
# MAGIC FROM dbo.quotes_gbp;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC COUNT(*) AS QuoteCount,
# MAGIC COUNT(DISTINCT QuoteID) AS UniqueQuotes
# MAGIC FROM Portfolio.Gold_LH.dbo.FactQuote;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT COUNT(*) AS MissingCustomers
# MAGIC FROM Portfolio.Gold_LH.dbo.FactQuote f
# MAGIC LEFT JOIN Portfolio.Gold_LH.dbo.DimCustomer d ON f.CustomerID = d.CustomerID
# MAGIC WHERE f.CustomerID IS NOT NULL
# MAGIC AND d.CustomerID IS NULL;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
