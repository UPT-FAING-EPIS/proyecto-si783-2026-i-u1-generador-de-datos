using DataGenerator.API.Models;

namespace DataGenerator.API.Generators;

public interface IDataGenerator
{
    string Name { get; }
    DataType DataType { get; }
    object Generate(Dictionary<string, object>? options = null);
    Dictionary<string, object> GetOptions(); // Opciones configurables
}