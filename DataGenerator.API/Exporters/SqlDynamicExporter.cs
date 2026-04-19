using DataGenerator.API.Models;
using System.Text;


namespace DataGenerator.API.Exporters;

public class SqlDynamicExporter : IDynamicExporter
{
    private readonly DatabaseType _databaseType;
    
    public SqlDynamicExporter(DatabaseType databaseType)
    {
        _databaseType = databaseType;
    }
    
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var sql = new StringBuilder();
        
        // CREATE TABLE
        sql.AppendLine(CreateTableStatement(request));
        sql.AppendLine();
        
        // INSERT statements
        foreach (var row in data)
        {
            sql.AppendLine(InsertStatement(row, request.TableName));
        }
        
        return sql.ToString();
    }
    
    private string CreateTableStatement(DynamicTableRequest request)
    {
        var columns = new List<string>();
        foreach (var col in request.Columns)
        {
            string sqlType = GetSqlType(col.Type, _databaseType);
            string nullable = col.IsNullable ? "" : " NOT NULL";
            columns.Add($"  {col.Name} {sqlType}{nullable}");
        }
        
        string tableName = _databaseType == DatabaseType.MySQL 
            ? $"`{request.TableName}`" 
            : $"\"{request.TableName}\"";
        
        return $"CREATE TABLE IF NOT EXISTS {tableName} (\n{string.Join(",\n", columns)}\n);";
    }
    
    private string InsertStatement(Dictionary<string, object> row, string tableName)
    {
        var columns = string.Join(", ", row.Keys);
        var values = string.Join(", ", row.Values.Select(v => FormatSqlValue(v, _databaseType)));
        
        string quotedTableName = _databaseType == DatabaseType.MySQL 
            ? $"`{tableName}`" 
            : $"\"{tableName}\"";
        
        return $"INSERT INTO {quotedTableName} ({columns}) VALUES ({values});";
    }
    
    private string FormatSqlValue(object value, DatabaseType dbType)
    {
        if (value == null || value == DBNull.Value)
            return "NULL";
        
        if (value is string str)
        {
            string escaped = str.Replace("'", "''");
            return $"'{escaped}'";
        }
        
        if (value is DateTime dt)
        {
            if (dbType == DatabaseType.MySQL)
                return $"'{dt:yyyy-MM-dd HH:mm:ss}'";
            else if (dbType == DatabaseType.PostgreSQL)
                return $"'{dt:yyyy-MM-dd HH:mm:ss}'";
            else if (dbType == DatabaseType.MicrosoftSQLServer)
                return $"'{dt:yyyy-MM-dd HH:mm:ss.fff}'";
        }
        
        if (value is bool b)
            return b ? "1" : "0";
        
        if (value is TimeSpan t)
            return $"'{t}'";
        
        return value.ToString() ?? "NULL";
    }
    
    private string GetSqlType(DataType type, DatabaseType dbType)
    {
        return (type, dbType) switch
        {
            (DataType.Integer, _) => "INT",
            (DataType.Decimal, _) => "DECIMAL(18,2)",
            (DataType.String, DatabaseType.MySQL) => "VARCHAR(255)",
            (DataType.String, DatabaseType.PostgreSQL) => "VARCHAR(255)",
            (DataType.String, DatabaseType.MicrosoftSQLServer) => "NVARCHAR(255)",
            (DataType.Boolean, _) => "BOOLEAN",
            (DataType.DateTime, _) => "DATETIME",
            (DataType.Date, _) => "DATE",
            (DataType.Time, _) => "TIME",
            (DataType.Guid, _) => "UNIQUEIDENTIFIER",
            (DataType.Email, _) => "VARCHAR(100)",
            (DataType.Phone, _) => "VARCHAR(20)",
            (DataType.Url, _) => "VARCHAR(255)",
            (DataType.IPv4, _) => "VARCHAR(15)",
            (DataType.Json, DatabaseType.MySQL) => "JSON",
            (DataType.Json, DatabaseType.PostgreSQL) => "JSONB",
            (DataType.Json, DatabaseType.MicrosoftSQLServer) => "NVARCHAR(MAX)",
            _ => "TEXT"
        };
    }
    
    public string GetFileExtension() => ".sql";
}