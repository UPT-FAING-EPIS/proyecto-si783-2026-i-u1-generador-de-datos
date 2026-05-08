using DataGenerator.API.Models;

namespace DataGenerator.API.Adapters;

public class OracleAdapter : IDatabaseAdapter
{
    public string Name => "Oracle";
    
    public string GetCreateTableScript(string tableName, List<ColumnDefinition> columns)
    {
        var columnsDef = columns.Select(col =>
        {
            string type = GetColumnType(col);
            string nullable = col.IsNullable ? "NULL" : "NOT NULL";
            return $"    \"{col.Name}\" {type} {nullable}";
        });
        
        return $@"CREATE TABLE ""{tableName}"" (
{string.Join(",\n", columnsDef)}
);";
    }
    
    public string GetColumnType(ColumnDefinition column)
    {
        return column.Type switch
        {
            DataType.Integer => "NUMBER(10)",
            DataType.Decimal => "NUMBER(15,2)",
            DataType.String => $"VARCHAR2({(column.MaxLength ?? 255)})",
            DataType.Boolean => "NUMBER(1)",
            DataType.DateTime => "TIMESTAMP",
            DataType.Date => "DATE",
            DataType.Time => "INTERVAL DAY TO SECOND",
            DataType.Guid => "RAW(16)",
            DataType.FullName => "VARCHAR2(100)",
            DataType.Email => "VARCHAR2(100)",
            DataType.Phone => "VARCHAR2(20)",
            DataType.City => "VARCHAR2(100)",
            DataType.Country => "VARCHAR2(100)",
            DataType.Text => "CLOB",
            DataType.Price => "NUMBER(12,2)",
            _ => "VARCHAR2(255)"
        };
    }
    
    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "NULL";
        
        return column.Type switch
        {
            DataType.String or DataType.Email or DataType.Phone or DataType.City 
                or DataType.Country or DataType.FullName => $"'{value.ToString().Replace("'", "''")}'",
            DataType.DateTime => $"TO_TIMESTAMP('{((DateTime)value):yyyy-MM-dd HH:mm:ss}', 'YYYY-MM-DD HH24:MI:SS')",
            DataType.Date => $"TO_DATE('{((DateTime)value):yyyy-MM-dd}', 'YYYY-MM-DD')",
            DataType.Boolean => (bool)value ? "1" : "0",
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
        return "User Id=user;Password=pass;Data Source=localhost:1521/XE;";
    }
}