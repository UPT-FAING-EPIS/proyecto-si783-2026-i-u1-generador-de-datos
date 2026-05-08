using System.Text.Json;
using Bogus;
using DataGenerator.API.Models;

namespace DataGenerator.API.Services;

public class DynamicDataGenerator : IDynamicDataGenerator
{
    private readonly Random _random = new Random();
    private readonly Faker _faker = new Faker("es");
    
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
        // ===== TIPOS BÁSICOS =====
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
        
        // ===== PERSONA =====
        case DataType.FullName:
            return _faker.Name.FullName();           // "Juan Pérez"
        case DataType.FirstName:
            return _faker.Name.FirstName();          // "Juan"
        case DataType.LastName:
            return _faker.Name.LastName();           // "Pérez"
        case DataType.UserName:
            return _faker.Internet.UserName();       // "juan.perez123"
        
        // ===== CONTACTO =====
        case DataType.Email:
            return GenerateEmail(column);
        case DataType.Phone:
            return _faker.Phone.PhoneNumber();       // "+54 11 1234-5678"
        case DataType.CellPhone:
            return _faker.Phone.PhoneNumber();       // "15-1234-5678"
        
        // ===== UBICACIÓN =====
        case DataType.City:
            return _faker.Address.City();             // "Buenos Aires"
        case DataType.Country:
            return _faker.Address.Country();          // "Argentina"
        case DataType.Address:
            return _faker.Address.FullAddress();      // "Av. Corrientes 1234"
        case DataType.ZipCode:
            return _faker.Address.ZipCode();          // "1425"
        case DataType.Latitude:
            return _faker.Address.Latitude();         // -34.6037
        case DataType.Longitude:
            return _faker.Address.Longitude();        // -58.3816
        
        // ===== INTERNET =====
        case DataType.IPv4:
            return _faker.Internet.IpAddress().ToString();
        case DataType.IPv6:
            return _faker.Internet.Ipv6Address();
        case DataType.Url:
            return _faker.Internet.Url();
        case DataType.DomainName:
            return _faker.Internet.DomainName();
        
        // ===== FINANZAS =====
        case DataType.CreditCardNumber:
            return _faker.Finance.CreditCardNumber();
        case DataType.Amount:
            return Math.Round(_faker.Random.Decimal(1, 10000), 2);
        case DataType.Currency:
            return _faker.Finance.Currency().Code;
        case DataType.IBAN:
            return _faker.Finance.Iban();
        
        // ===== EMPRESA =====
        case DataType.CompanyName:
            return _faker.Company.CompanyName();
        case DataType.JobTitle:
            return _faker.Name.JobTitle();
        case DataType.Department:
            return _faker.Commerce.Department();
        
        // ===== PRODUCTO =====
        case DataType.ProductName:
            return _faker.Commerce.ProductName();
        case DataType.ProductDescription:
            return _faker.Commerce.ProductDescription();
        case DataType.Price:
            return decimal.Parse(_faker.Commerce.Price());
        case DataType.SKU:
            return _faker.Commerce.Ean8();
        
        // ===== TEXTO =====
        case DataType.Text:
            return _faker.Lorem.Text();
        case DataType.Paragraph:
            return _faker.Lorem.Paragraph();
        case DataType.Sentence:
            return _faker.Lorem.Sentence();
        case DataType.Word:
            return _faker.Lorem.Word();
        
        // ===== IDENTIFICADORES =====
        case DataType.UUID:
            return Guid.NewGuid();
        case DataType.Cuit:
            return $"{_random.Next(20, 35)}-{_random.Next(10000000, 99999999)}-{_random.Next(0, 9)}";
        case DataType.Rfc:
            return $"{_faker.Random.String2(4, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")}{_random.Next(100101, 991231)}-{_faker.Random.String2(3, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")}";
        case DataType.Dni:
            return _random.Next(10000000, 99999999).ToString();
        
        // ===== OTROS =====
        case DataType.Color:
            return _faker.Commerce.Color();           // "rojo", "azul", "verde"
        case DataType.ImageUrl:
            return _faker.Image.PicsumUrl();
        case DataType.Enum:
            return GenerateEnum(column);
        case DataType.Json:
            return GenerateJson();
        case DataType.Null:
            return null;
        
        default:
            return _faker.Lorem.Word();
    }
}
    private object GenerateEmail(ColumnDefinition column)
    {
        // Intentar obtener dominio de las opciones si existe
        string domain = null;
        
        // Si la columna tiene PossibleValues, usarlo como dominio
        if (column.PossibleValues != null && column.PossibleValues.Any())
        {
            domain = column.PossibleValues[_random.Next(column.PossibleValues.Count)];
        }
        
        if (!string.IsNullOrEmpty(domain))
        {
            string userName = _faker.Internet.UserName();
            return $"{userName}@{domain}";
        }
        
        return _faker.Internet.Email();
    }
    
    private object GenerateJson()
    {
        return new 
        { 
            id = _random.Next(1, 10000), 
            name = _faker.Lorem.Word(),
            created = _faker.Date.Past()
        };
    }
    
    private object GenerateInteger(ColumnDefinition column)
    {
        int min = 1;
        int max = 1000;
        
        if (column.MinValue != null)
        {
            try
            {
                if (column.MinValue is JsonElement jsonMin)
                    min = jsonMin.GetInt32();
                else
                    min = Convert.ToInt32(column.MinValue);
            }
            catch
            {
                min = 1;
            }
        }
        
        if (column.MaxValue != null)
        {
            try
            {
                if (column.MaxValue is JsonElement jsonMax)
                    max = jsonMax.GetInt32();
                else
                    max = Convert.ToInt32(column.MaxValue);
            }
            catch
            {
                max = 1000;
            }
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
            try
            {
                if (column.MinValue is JsonElement jsonMin)
                    min = jsonMin.GetDecimal();
                else
                    min = Convert.ToDecimal(column.MinValue);
            }
            catch
            {
                min = 0;
            }
        }
        
        if (column.MaxValue != null)
        {
            try
            {
                if (column.MaxValue is JsonElement jsonMax)
                    max = jsonMax.GetDecimal();
                else
                    max = Convert.ToDecimal(column.MaxValue);
            }
            catch
            {
                max = 1000;
            }
        }
        
        if (min > max) (min, max) = (max, min);
        return Math.Round((decimal)(_random.NextDouble() * (double)(max - min) + (double)min), 2);
    }
    
   private object GenerateString(ColumnDefinition column)
{
    int maxLength = 100;
    
    // MaxLength es int?, no necesita conversión compleja
    if (column.MaxLength.HasValue && column.MaxLength.Value > 0)
    {
        maxLength = column.MaxLength.Value;
    }
    
    if (maxLength <= 0) maxLength = 100;
    
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