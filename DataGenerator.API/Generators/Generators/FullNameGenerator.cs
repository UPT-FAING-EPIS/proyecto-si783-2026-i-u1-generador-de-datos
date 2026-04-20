using Bogus;
using DataGenerator.API.Models;

namespace DataGenerator.API.Generators.Generators;

public class FullNameGenerator : IDataGenerator
{
    public string Name => "Nombre Completo";
    public DataType DataType => DataType.FullName;
    private readonly Faker _faker = new Faker("es");
    
    public object Generate(Dictionary<string, object>? options = null)
    {
        bool includePrefix = options?.ContainsKey("includePrefix") == true 
                             ? (bool)options["includePrefix"] : false;
        
        if (includePrefix)
            return _faker.Name.Prefix() + " " + _faker.Name.FullName();
        
        return _faker.Name.FullName();
    }
    
    public Dictionary<string, object> GetOptions()
    {
        return new Dictionary<string, object>
        {
            { "includePrefix", false },
            { "prefixOptions", new[] { "Sr.", "Sra.", "Dr.", "Ing." } }
        };
    }
}