using DataGenerator.API.Models;

namespace DataGenerator.API.Adapters;

public class RedisAdapter : IDatabaseAdapter
{
    public string Name => "Redis";
    
    public string GetCreateTableScript(string tableName, List<ColumnDefinition> columns)
    {
        return $"// Redis keyspace '{tableName}' - No DDL needed";
    }
    
    public string GetColumnType(ColumnDefinition column)
    {
        return "string";
    }
    
    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "null";
        return $"\"{value}\"";
    }
    
    public string GetInsertScript(string tableName, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
        var commands = new List<string>();
        
        // Obtener el ID (asumimos primera columna como key)
        var keyColumn = columns.FirstOrDefault();
        var key = keyColumn != null ? row[keyColumn.Name]?.ToString() : Guid.NewGuid().ToString();
        
        foreach (var col in columns)
        {
            commands.Add($"HSET {tableName}:{key} {col.Name} {FormatValue(row[col.Name], col)}");
        }
        
        return string.Join("\n", commands);
    }
    
    public string GetConnectionStringExample()
    {
        return "localhost:6379";
    }
}