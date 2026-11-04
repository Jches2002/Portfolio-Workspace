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
# META           "id": "eecd10a4-6028-47b4-b6ae-8b4b4baf9917"
# META         },
# META         {
# META           "id": "8adcea99-5f6c-4c24-92cd-a7f2742d5955"
# META         }
# META       ]
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC DESCRIBE dbo.platform_a_quotes;
# MAGIC 
# MAGIC DESCRIBE dbo.platform_b_quotes;
# MAGIC 
# MAGIC DESCRIBE dbo.platform_c_quotes;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE dbo.quotes
# MAGIC USING DELTA AS
# MAGIC SELECT * FROM dbo.platform_a_quotes
# MAGIC UNION ALL
# MAGIC SELECT * FROM dbo.platform_b_quotes
# MAGIC UNION ALL
# MAGIC SELECT * FROM dbo.platform_c_quotes;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC SourcePlatform,
# MAGIC COUNT(*) AS QuoteCount
# MAGIC FROM dbo.quotes
# MAGIC GROUP BY SourcePlatform
# MAGIC ORDER BY SourcePlatform;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT COUNT(*) AS TotalQuotes
# MAGIC FROM dbo.quotes;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_exchange_rates = (spark.read.option("header", "true") .option("inferSchema", "true") .csv("abfss://Portfolio@onelake.dfs.fabric.microsoft.com/Bronze_LH.Lakehouse/Files/Quotes/Dimensions/exchange_rates.csv")
)

df_exchange_rates.createOrReplaceTempView("exchange_rates")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE dbo.quotes_gbp
# MAGIC USING DELTA AS
# MAGIC SELECT
# MAGIC q.*,
# MAGIC e.GBP_Rate AS ExchangeRate,
# MAGIC CAST(q.QuotedCostLocal * e.GBP_Rate AS DECIMAL(18,2)) AS QuotedCostGBP,
# MAGIC CAST(q.QuotedSellLocal * e.GBP_Rate AS DECIMAL(18,2)) AS QuotedSellGBP,
# MAGIC CAST((q.QuotedSellLocal - q.QuotedCostLocal) * e.GBP_Rate AS DECIMAL(18,2)) AS GrossProfitGBP,
# MAGIC CAST((q.QuotedSellLocal - q.QuotedCostLocal) / q.QuotedSellLocal AS DECIMAL(18,4)) AS GrossProfitMargin
# MAGIC FROM dbo.quotes q
# MAGIC LEFT JOIN exchange_rates e ON q.QuoteDate = e.Rate_Date AND q.Currency = e.Currency;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC Currency,
# MAGIC COUNT(*) AS QuoteCount,
# MAGIC SUM(CASE WHEN ExchangeRate IS NULL THEN 1 ELSE 0 END) AS MissingRates
# MAGIC FROM dbo.quotes_gbp
# MAGIC GROUP BY Currency
# MAGIC ORDER BY Currency;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC Currency,
# MAGIC QuotedCostLocal,
# MAGIC QuotedSellLocal,
# MAGIC ExchangeRate,
# MAGIC QuotedCostGBP,
# MAGIC QuotedSellGBP,
# MAGIC GrossProfitGBP,
# MAGIC GrossProfitMargin
# MAGIC FROM dbo.quotes_gbp
# MAGIC LIMIT 20;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC SourcePlatform,
# MAGIC COUNT(*) AS QuoteCount,
# MAGIC SUM(QuotedSellGBP) AS QuotedSellGBP,
# MAGIC SUM(GrossProfitGBP) AS GrossProfitGBP
# MAGIC FROM dbo.quotes_gbp
# MAGIC GROUP BY SourcePlatform
# MAGIC ORDER BY SourcePlatform;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
