namespace DataGenerator.API.Models;

public enum DataType
{
    // Tipos básicos
    Integer,
    Decimal,
    String,
    Boolean,
    DateTime,
    Date,
    Time,
    Guid,
    
    // Tipos especiales
    Email,
    Phone,
    Url,
    IPv4,
    IPv6,
    
    // Tipos para selección
    Enum,
    
    // Tipos para JSON
    Json,
    
    // Nulos
    Null
}