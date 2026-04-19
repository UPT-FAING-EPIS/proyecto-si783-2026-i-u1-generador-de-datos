using System.Text.Json;
using Bogus;
using DataGenerator.API.Models;

namespace DataGenerator.API.Services;

public class DynamicDataGenerator : IDynamicDataGenerator
{
    private readonly Random _random = new Random();
    private readonly Faker _faker = new Faker("es"); // Español
    
    public List<Dictionary<string, object>> GenerateData(DynamicTableRequest request)
    {
        var data = new List<Dictionary<string, object>>();
        
        for (int i = 0; i < request.RecordCount; i++)
        {
            var row = new Dictionary<string, object>();
            foreach (var column in request.Columns)
            {
                row[column.Name] = GenerateValue(column);
            }
            data.Add(row);
        }
        
        return data;
    }
    
    private object GenerateValue(ColumnDefinition column)
    {
        // Si es nullable, 10% de probabilidad de ser null
        if (column.IsNullable && _random.Next(100) < 10)
        {
            return null;
        }
        
        // Generar según el tipo de dato
        switch (column.Type)
        {
            case DataType.Integer:
                return GenerateInteger(column);
            case DataType.Decimal:
                return GenerateDecimal(column);
            case DataType.String:
                return GenerateString(column);
            case DataType.Boolean:
                return _faker.Random.Bool();
            case DataType.DateTime:
                return _faker.Date.Past(5);
            case DataType.Date:
                return _faker.Date.PastDateOnly(5);
            case DataType.Time:
                return _faker.Date.Timespan();
            case DataType.Guid:
                return Guid.NewGuid();
            case DataType.Email:
                return _faker.Internet.Email();
            case DataType.Phone:
                return _faker.Phone.PhoneNumber();
            case DataType.Url:
                return _faker.Internet.Url();
            case DataType.IPv4:
                return _faker.Internet.IpAddress().ToString();
            case DataType.IPv6:
                return _faker.Internet.Ipv6Address();
            case DataType.Enum:
                return GenerateEnum(column);
            case DataType.Json:
                return new { id = _random.Next(1000), name = _faker.Lorem.Word() };
            case DataType.Null:
                return null;
            default:
                return _faker.Lorem.Word();
        }
    }
    
    private object GenerateInteger(ColumnDefinition column)
    {
        int min = 1;
        int max = 1000;
        
        if (column.MinValue != null)
        {
            if (column.MinValue is JsonElement jsonMin)
                min = jsonMin.GetInt32();
            else
                min = Convert.ToInt32(column.MinValue);
        }
        
        if (column.MaxValue != null)
        {
            if (column.MaxValue is JsonElement jsonMax)
                max = jsonMax.GetInt32();
            else
                max = Convert.ToInt32(column.MaxValue);
        }
        
        if (min > max) (min, max) = (max, min);
        return _random.Next(min, max + 1);
    }
    
    private object GenerateDecimal(ColumnDefinition column)
    {
        decimal min = 0;
        decimal max = 1000;
        
        if (column.MinValue != null)
        {
            if (column.MinValue is JsonElement jsonMin)
                min = jsonMin.GetDecimal();
            else
                min = Convert.ToDecimal(column.MinValue);
        }
        
        if (column.MaxValue != null)
        {
            if (column.MaxValue is JsonElement jsonMax)
                max = jsonMax.GetDecimal();
            else
                max = Convert.ToDecimal(column.MaxValue);
        }
        
        if (min > max) (min, max) = (max, min);
        return Math.Round(_faker.Random.Decimal(min, max), 2);
    }
    
  private object GenerateString(ColumnDefinition column)
{
    int maxLength = 100;
    
    // Como MaxLength es int?, lo usamos directamente
    if (column.MaxLength.HasValue)
    {
        maxLength = column.MaxLength.Value;
    }
    
    string result = _faker.Lorem.Word();
    
    if (result.Length > maxLength)
        result = result.Substring(0, maxLength);
    
    return result;
}
    private object GenerateEnum(ColumnDefinition column)
    {
        if (column.PossibleValues != null && column.PossibleValues.Any())
        {
            return column.PossibleValues[_random.Next(column.PossibleValues.Count)];
        }
        return _faker.Lorem.Word();
    }
}