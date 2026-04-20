using Bogus;
using DataGenerator.API.Models;

namespace DataGenerator.API.Generators.Generators;

public class CityGenerator : IDataGenerator
{
    public string Name => "Ciudad";
    public DataType DataType => DataType.City;
    private readonly Faker _faker = new Faker("es");
    
    public object Generate(Dictionary<string, object>? options = null)
    {
        string country = options?.ContainsKey("country") == true 
                         ? options["country"].ToString() 
                         : null;
        
        if (country == "Argentina")
            return _faker.Address.City();
        
        if (country == "Mexico")
            return _faker.Address.City();
        
        return _faker.Address.City();
    }
    
    public Dictionary<string, object> GetOptions()
    {
        return new Dictionary<string, object>
        {
            { "country", "Argentina" },
            { "countries", new[] { "Argentina", "Mexico", "Spain", "Colombia" } }
        };
    }
}