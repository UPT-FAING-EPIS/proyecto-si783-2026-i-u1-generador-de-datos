/* public class MongoDbAdapter : IDatabaseAdapter
{
    public string Name => "MongoDB";
    
    public string GetCreateTableScript(string tableName, List<ColumnDefinition> columns)
    {
        // MongoDB no necesita CREATE TABLE, es schemaless
        return $"// Colección '{tableName}' se creará automáticamente al insertar";
    }
    
    public string GetInsertScript(string tableName, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
        var jsonDoc = new Dictionary<string, object>();
        foreach (var col in columns)
        {
            jsonDoc[col.Name] = row[col.Name];
        }
        return $"db.{tableName}.insertOne({System.Text.Json.JsonSerializer.Serialize(jsonDoc)});";
    }
    
    // ... otros métodos
} */