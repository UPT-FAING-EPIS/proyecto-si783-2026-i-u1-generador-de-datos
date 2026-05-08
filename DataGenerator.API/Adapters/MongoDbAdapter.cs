using DataGenerator.API.Models;
using System.Text.Json;

namespace DataGenerator.API.Adapters;

public class MongoDbAdapter : IDatabaseAdapter
{
    public string Name => "MongoDB";
    
    public string GetCreateTableScript(string tableName, List<ColumnDefinition> columns)
    {
        // MongoDB no tiene DDL, es schemaless
        return $"// MongoDB collection '{tableName}' - No DDL needed\n// Use: db.createCollection(\"{tableName}\")";
    }
    
    public string GetColumnType(ColumnDefinition column)
    {
        // MongoDB es dinámico
        return "any";
    }
    
    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "null";
        
        return column.Type switch
        {
            DataType.String or DataType.Email or DataType.Phone or DataType.City 
                or DataType.Country or DataType.FullName => $"\"{value.ToString().Replace("\"", "\\\"")}\"",
            DataType.Boolean => value.ToString()?.ToLower() ?? "false",
            DataType.DateTime or DataType.Date => $"ISODate(\"{((DateTime)value):yyyy-MM-ddTHH:mm:ss}Z\")",
            DataType.Integer or DataType.Decimal or DataType.Price => value.ToString() ?? "0",
            _ => $"\"{value}\""
        };
    }
    
    public string GetInsertScript(string tableName, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
        var bsonDoc = string.Join(", ", columns.Select(c => 
            $"    {c.Name}: {FormatValue(row[c.Name], c)}"));
        
        return $"db.{tableName}.insertOne({{\n{bsonDoc}\n}});";
    }
    
    public string GetConnectionStringExample()
    {
        return "mongodb://localhost:27017";
    }
}