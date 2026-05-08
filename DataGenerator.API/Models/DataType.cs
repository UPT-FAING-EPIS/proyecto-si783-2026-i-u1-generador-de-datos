namespace DataGenerator.API.Models;

public enum DataType
{
    // Tipos básicos (ya existentes)
    Integer,
    Decimal,
    String,
    Boolean,
    DateTime,
    Date,
    Time,
    Guid,
    
    // ===== NUEVOS GENERADORES SEMÁNTICOS =====
    // Persona
    FullName,
    FirstName,
    LastName,
    UserName,
    
    // Contacto
    Email,
    Phone,
    CellPhone,
    
    // Ubicación
    City,
    Country,
    Address,
    ZipCode,
    Latitude,
    Longitude,
    
    // Internet
    IPv4,
    IPv6,
    Url,
    DomainName,
    
    // Finanzas
    CreditCardNumber,
    CreditCardType,
    Amount,
    Currency,
    IBAN,
    
    // Empresa
    CompanyName,
    JobTitle,
    Department,
    
    // Producto
    ProductName,
    ProductDescription,
    Price,
    SKU,
    
    // Texto
    Text,
    Paragraph,
    Sentence,
    Word,
    
    // Identificadores
    UUID,
    Cuit,      // Argentina
    Rfc,       // México
    Dni,       // España/Argentina
    
    // Otros
    Color,
    ImageUrl,
    DateRange,
    Enum,
    Json,
    Null
}