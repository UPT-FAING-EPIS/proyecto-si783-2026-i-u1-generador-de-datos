using DataGenerator.API.Models;

namespace DataGenerator.API.Adapters;

public class MySqlAdapter : IDatabaseAdapter
{
    public string Name => "MySQL";
    
    public string GetCreateTableScript(string tableName, List<ColumnDefinition> columns)
    {
        var columnsDef = columns.Select(col =>
        {
            string type = GetColumnType(col);
            string nullable = col.IsNullable ? "NULL" : "NOT NULL";
            return $"    `{col.Name}` {type} {nullable}";
        });
        
        return $@"CREATE TABLE IF NOT EXISTS `{tableName}` (
{string.Join(",\n", columnsDef)}
);";
    }
    
    public string GetColumnType(ColumnDefinition column)
    {
        return column.Type switch
        {
            DataType.Integer => "INT",
            DataType.Decimal => "DECIMAL(10,2)",
            DataType.String => $"VARCHAR({(column.MaxLength ?? 255)})",
            DataType.Boolean => "BOOLEAN",
            DataType.DateTime => "DATETIME",
            DataType.Date => "DATE",
            DataType.Time => "TIME",
            DataType.Guid => "CHAR(36)",
            DataType.Email => "VARCHAR(100)",
            DataType.Phone => "VARCHAR(20)",
            DataType.City => "VARCHAR(100)",
            DataType.FullName => "VARCHAR(100)",
            DataType.CreditCardNumber => "VARCHAR(20)",
            DataType.IPv4 => "VARCHAR(15)",
            _ => "TEXT"
        };
    }
    
    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "NULL";
        
        return column.Type switch
        {
            DataType.String or DataType.Email or DataType.Phone or DataType.City 
                or DataType.FullName or DataType.CreditCardNumber or DataType.IPv4 
                or DataType.Guid => $"'{value.ToString().Replace("'", "''")}'",
            DataType.DateTime => $"'{((DateTime)value):yyyy-MM-dd HH:mm:ss}'",
            DataType.Date => $"'{((DateTime)value):yyyy-MM-dd}'",
            DataType.Time => $"'{((TimeSpan)value)}'",
            DataType.Boolean => (bool)value ? "1" : "0",
            _ => value.ToString()
        };
    }
    
    public string GetInsertScript(string tableName, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
        var columnNames = columns.Select(c => $"`{c.Name}`");
        var values = columns.Select(c => FormatValue(row[c.Name], c));
        
        return $"INSERT INTO `{tableName}` ({string.Join(", ", columnNames)}) VALUES ({string.Join(", ", values)});";
    }
    
    public string GetConnectionStringExample()
    {
        return "Server=localhost;Database=mi_db;User=root;Password=123456;";
    }
}