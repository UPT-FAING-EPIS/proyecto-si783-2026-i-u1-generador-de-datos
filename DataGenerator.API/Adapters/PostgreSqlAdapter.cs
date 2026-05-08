using DataGenerator.API.Models;

namespace DataGenerator.API.Adapters;

public class PostgreSqlAdapter : IDatabaseAdapter
{
    public string Name => "PostgreSQL";
    
    public string GetCreateTableScript(string tableName, List<ColumnDefinition> columns)
    {
        var columnsDef = columns.Select(col =>
        {
            string type = GetColumnType(col);
            string nullable = col.IsNullable ? "NULL" : "NOT NULL";
            return $"    \"{col.Name}\" {type} {nullable}";
        });
        
        return $@"CREATE TABLE IF NOT EXISTS ""{tableName}"" (
{string.Join(",\n", columnsDef)}
);";
    }
    
    public string GetColumnType(ColumnDefinition column)
    {
        return column.Type switch
        {
            DataType.Integer => "INTEGER",
            DataType.Decimal => "DECIMAL(10,2)",
            DataType.String => $"VARCHAR({(column.MaxLength ?? 255)})",
            DataType.Boolean => "BOOLEAN",
            DataType.DateTime => "TIMESTAMP",
            DataType.Date => "DATE",
            DataType.Time => "TIME",
            DataType.Guid => "UUID",
            DataType.FullName => "VARCHAR(100)",
            DataType.Email => "VARCHAR(100)",
            DataType.Phone => "VARCHAR(20)",
            DataType.City => "VARCHAR(100)",
            DataType.Country => "VARCHAR(100)",
            DataType.Address => "TEXT",
            DataType.CreditCardNumber => "VARCHAR(20)",
            DataType.CompanyName => "VARCHAR(100)",
            DataType.ProductName => "VARCHAR(100)",
            DataType.Price => "DECIMAL(10,2)",
            DataType.Text => "TEXT",
            DataType.UUID => "UUID",
            _ => "TEXT"
        };
    }
    
    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "NULL";
        
        return column.Type switch
        {
            DataType.String or DataType.Email or DataType.Phone or DataType.City 
                or DataType.Country or DataType.FullName or DataType.CompanyName 
                or DataType.ProductName or DataType.Address or DataType.Text => $"'{value.ToString().Replace("'", "''")}'",
            DataType.DateTime => $"'{((DateTime)value):yyyy-MM-dd HH:mm:ss}'",
            DataType.Date => $"'{((DateTime)value):yyyy-MM-dd}'",
            DataType.Time => $"'{((TimeSpan)value)}'",
            DataType.Boolean => (bool)value ? "true" : "false",
            DataType.Guid => $"'{value}'",
            DataType.UUID => $"'{value}'",
            _ => value.ToString() ?? "NULL"
        };
    }
    
    public string GetInsertScript(string tableName, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
        var columnNames = columns.Select(c => $"\"{c.Name}\"");
        var values = columns.Select(c => FormatValue(row[c.Name], c));
        
        return $"INSERT INTO \"{tableName}\" ({string.Join(", ", columnNames)}) VALUES ({string.Join(", ", values)});";
    }
    
    public string GetConnectionStringExample()
    {
        return "Host=localhost;Database=mi_db;Username=postgres;Password=123456;";
    }
}