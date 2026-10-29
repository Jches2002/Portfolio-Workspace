[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Customers_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared DimCustomers = let
  Source = Excel.Workbook(Web.Contents("https://xpandlhr-my.sharepoint.com/personal/jack_chesney_xpandlogistics_co_uk/Documents/Microsoft%20Fabric/BI/Exective%20project/Executive_Financial_Dashboard_Test_Data_v3_OperatingProfit.xlsx"), null, true),
  #"Navigation 1" = Source{[Item = "Customers", Kind = "Sheet"]}[Data],
  #"Promoted headers" = Table.PromoteHeaders(#"Navigation 1", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"CustomerID", type text}, {"CustomerName", type text}, {"Industry", type text}, {"Region", type text}, {"Segment", type text}})
in
  #"Changed column type";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "DimBranches_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared DimBranches = let
  Source = Excel.Workbook(Web.Contents("https://xpandlhr-my.sharepoint.com/personal/jack_chesney_xpandlogistics_co_uk/Documents/Microsoft%20Fabric/BI/Exective%20project/Executive_Financial_Dashboard_Test_Data_v3_OperatingProfit.xlsx"), null, true),
  #"Navigation 1" = Source{[Item = "Branches", Kind = "Sheet"]}[Data],
  #"Promoted headers" = Table.PromoteHeaders(#"Navigation 1", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"BranchID", type text}, {"BranchName", type text}, {"Region", type text}, {"Country", type text}})
in
  #"Changed column type";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "DimServices_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared DimServices = let
  Source = Excel.Workbook(Web.Contents("https://xpandlhr-my.sharepoint.com/personal/jack_chesney_xpandlogistics_co_uk/Documents/Microsoft%20Fabric/BI/Exective%20project/Executive_Financial_Dashboard_Test_Data_v3_OperatingProfit.xlsx"), null, true),
  #"Navigation 1" = Source{[Item = "Services", Kind = "Sheet"]}[Data],
  #"Changed column type" = Table.TransformColumnTypes(#"Navigation 1", {{"Column1", type text}, {"Column2", type text}, {"Column3", type text}}),
  #"Promoted headers" = Table.PromoteHeaders(#"Changed column type", [PromoteAllScalars = true])
in
  #"Promoted headers";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "FactFinancialTransactions_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared FactFinancialTransactions = let
  Source = Excel.Workbook(Web.Contents("https://xpandlhr-my.sharepoint.com/personal/jack_chesney_xpandlogistics_co_uk/Documents/Microsoft%20Fabric/BI/Exective%20project/Executive_Financial_Dashboard_Test_Data_v3_OperatingProfit.xlsx"), null, true),
  #"Navigation 1" = Source{[Item = "FinancialTransactions", Kind = "Sheet"]}[Data],
  #"Promoted headers" = Table.PromoteHeaders(#"Navigation 1", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"TransactionID", type text}, {"InvoiceDate", type date}, {"CustomerID", type text}, {"BranchID", type text}, {"ServiceID", type text}, {"RevenueGBP", type number}, {"DirectCostGBP", type number}})
in
  #"Changed column type";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "FactBudget_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared FactBudget = let
  Source = Excel.Workbook(Web.Contents("https://xpandlhr-my.sharepoint.com/personal/jack_chesney_xpandlogistics_co_uk/Documents/Microsoft%20Fabric/BI/Exective%20project/Executive_Financial_Dashboard_Test_Data_v3_OperatingProfit.xlsx"), null, true),
  #"Navigation 1" = Source{[Item = "Budget", Kind = "Sheet"]}[Data],
  #"Promoted headers" = Table.PromoteHeaders(#"Navigation 1", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"MonthStart", type date}, {"BranchID", type text}, {"ServiceID", type text}, {"BudgetRevenueGBP", type number}, {"BudgetCostGBP", type number}})
in
  #"Changed column type";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "FactOperatingExpenses_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared FactOperatingExpenses = let
  Source = Excel.Workbook(Web.Contents("https://xpandlhr-my.sharepoint.com/personal/jack_chesney_xpandlogistics_co_uk/Documents/Microsoft%20Fabric/BI/Exective%20project/Executive_Financial_Dashboard_Test_Data_v3_OperatingProfit.xlsx"), null, true),
  #"Navigation 1" = Source{[Item = "OperatingExpenses", Kind = "Sheet"]}[Data],
  #"Promoted headers" = Table.PromoteHeaders(#"Navigation 1", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"MonthStart", type date}, {"BranchID", type text}, {"ExpenseCategoryID", type text}, {"ExpenseCategory", type text}, {"ExpenseGroup", type text}, {"ActualOverheadGBP", type number}})
in
  #"Changed column type";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "FactOverheadBudget_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared FactOverheadBudget = let
  Source = Excel.Workbook(Web.Contents("https://xpandlhr-my.sharepoint.com/personal/jack_chesney_xpandlogistics_co_uk/Documents/Microsoft%20Fabric/BI/Exective%20project/Executive_Financial_Dashboard_Test_Data_v3_OperatingProfit.xlsx"), null, true),
  #"Navigation 1" = Source{[Item = "OverheadBudget", Kind = "Sheet"]}[Data],
  #"Promoted headers" = Table.PromoteHeaders(#"Navigation 1", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"MonthStart", type date}, {"BranchID", type text}, {"ExpenseCategoryID", type text}, {"ExpenseCategory", type text}, {"ExpenseGroup", type text}, {"BudgetOverheadGBP", type number}})
in
  #"Changed column type";
shared Customers_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "8adcea99-5f6c-4c24-92cd-a7f2742d5955"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "DimCustomers", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "DimDate_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared DimDate = let
  Source = let
    Source = #date(2024, 1, 1),
    EndDate = Date.EndOfYear(Date.From(DateTime.LocalNow())),
    Duration = Duration.Days(EndDate - Source) + 1,
    Dates = List.Dates(Source, Duration, #duration(1, 0, 0, 0))
in
    Dates,
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Renamed columns" = Table.RenameColumns(#"Converted to table", {{"Column1", "Date"}}),
  #"Added custom 2" = Table.TransformColumnTypes(Table.AddColumn(#"Renamed columns", "Year", each Date.Year([Date])), {{"Year", type text}}),
  #"Added custom 1" = Table.TransformColumnTypes(Table.AddColumn(#"Added custom 2", "Qtr", each Date.QuarterOfYear([Date])), {{"Qtr", Int64.Type}}),
  #"Added custom" = Table.TransformColumnTypes(Table.AddColumn(#"Added custom 1", "Month", each Date.Month([Date])), {{"Month", Int64.Type}}),
  #"Added custom 3" = Table.TransformColumnTypes(Table.AddColumn(#"Added custom", "MonthName", each Date.MonthName([Date])), {{"MonthName", type text}}),
  #"Added custom 6" = Table.TransformColumnTypes(Table.AddColumn(#"Added custom 3", "Week", each Date.WeekOfYear([Date])), {{"Week", Int64.Type}}),
  #"Added custom 5" = Table.TransformColumnTypes(Table.AddColumn(#"Added custom 6", "DayName", each Date.DayOfWeekName([Date])), {{"DayName", type text}}),
  #"Added custom 4" = Table.AddColumn(#"Added custom 5","Day",each Date.DayOfWeek([Date], Day.Monday) + 1, Int64.Type),
  #"Added custom 7" = Table.TransformColumnTypes(Table.AddColumn(#"Added custom 4", "YearMonth", each Date.ToText([Date], "MMM-yyyy")), {{"YearMonth", type text}})
in
  #"Added custom 7";
shared DimDate_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "8adcea99-5f6c-4c24-92cd-a7f2742d5955"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "DimDate", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared FactOverheadBudget_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "8adcea99-5f6c-4c24-92cd-a7f2742d5955"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "FactOverheadBudget", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared FactOperatingExpenses_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "8adcea99-5f6c-4c24-92cd-a7f2742d5955"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "FactOperatingExpenses", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared FactBudget_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "8adcea99-5f6c-4c24-92cd-a7f2742d5955"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "FactBudget", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared FactFinancialTransactions_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "8adcea99-5f6c-4c24-92cd-a7f2742d5955"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "FactFinancialTransactions", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared DimServices_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "8adcea99-5f6c-4c24-92cd-a7f2742d5955"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "DimServices", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared DimBranches_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "8adcea99-5f6c-4c24-92cd-a7f2742d5955"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "DimBranches", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
