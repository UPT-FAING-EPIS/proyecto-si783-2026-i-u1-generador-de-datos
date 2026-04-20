using Bogus;
using DataGenerator.API.Models;

namespace DataGenerator.API.Generators.Generators;

public class EmailGenerator : IDataGenerator
{
    public string Name => "Correo Electrónico";
    public DataType DataType => DataType.Email;
    private readonly Faker _faker = new Faker("es");
    
   public object Generate(Dictionary<string, object>? options = null)
{
    string domain = options?.ContainsKey("domain") == true 
                    ? options["domain"]?.ToString() 
                    : null;
    
    if (!string.IsNullOrEmpty(domain))
    {
        // Bogus no permite dominio personalizado directamente
        string userName = _faker.Internet.UserName();
        return $"{userName}@{domain}";
    }
    
    return _faker.Internet.Email();
}
    
    public Dictionary<string, object> GetOptions()
    {
        return new Dictionary<string, object>
        {
            { "domain", "ejemplo.com" },
            { "allowCustomDomain", true }
        };
    }
}