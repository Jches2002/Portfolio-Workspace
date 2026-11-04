[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
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
  #"Added custom 7" = Table.TransformColumnTypes(Table.AddColumn(#"Added custom 4", "YearMonth", each Date.ToText([Date], "MMM-yyyy")), {{"YearMonth", type text}}),
  #"Changed column type" = Table.TransformColumnTypes(#"Added custom 7", {{"Date", type date}})
in
  #"Changed column type";
shared DimDate_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "af8654ea-6e65-4a3a-95a1-fcfb5f99f885"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "808cf73d-b495-4ed5-832e-60052054b64a"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "DimDate", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
