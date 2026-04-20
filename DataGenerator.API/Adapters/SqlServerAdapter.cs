using DataGenerator.API.Models;

namespace DataGenerator.API.Adapters;

public class SqlServerAdapter : IDatabaseAdapter
{
    public string Name => "SQL Server";
    
    public string GetCreateTableScript(string tableName, List<ColumnDefinition> columns)
    {
        var columnsDef = columns.Select(col =>
        {
            string type = GetColumnType(col);
            string nullable = col.IsNullable ? "NULL" : "NOT NULL";
            return $"    [{col.Name}] {type} {nullable}";
        });
        
        return $@"CREATE TABLE [{tableName}] (
{string.Join(",\n", columnsDef)}
);";
    }
    
    public string GetColumnType(ColumnDefinition column)
    {
        return column.Type switch
        {
            DataType.Integer => "INT",
            DataType.Decimal => "DECIMAL(10,2)",
            DataType.String => $"NVARCHAR({(column.MaxLength ?? 255)})",
            DataType.Boolean => "BIT",
            DataType.DateTime => "DATETIME2",
            DataType.Date => "DATE",
            DataType.Time => "TIME",
            DataType.Guid => "UNIQUEIDENTIFIER",
            _ => "NVARCHAR(MAX)"
        };
    }
    
    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "NULL";
        
        return column.Type switch
        {
            DataType.String or DataType.Email or DataType.Phone => $"N'{value.ToString().Replace("'", "''")}'",
            DataType.DateTime => $"'{((DateTime)value):yyyy-MM-dd HH:mm:ss}'",
            DataType.Boolean => (bool)value ? "1" : "0",
            DataType.Guid => $"'{value}'",
            _ => value.ToString()
        };
    }
    
    public string GetInsertScript(string tableName, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
        var columnNames = columns.Select(c => $"[{c.Name}]");
        var values = columns.Select(c => FormatValue(row[c.Name], c));
        
        return $"INSERT INTO [{tableName}] ({string.Join(", ", columnNames)}) VALUES ({string.Join(", ", values)});";
    }
    
    public string GetConnectionStringExample()
    {
        return "Server=localhost;Database=mi_db;Trusted_Connection=true;";
    }
}