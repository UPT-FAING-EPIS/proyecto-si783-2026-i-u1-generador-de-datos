using DataGenerator.API.Models;

namespace DataGenerator.API.Services;

public interface IDynamicDataGenerator
{
    List<Dictionary<string, object>> GenerateData(DynamicTableRequest request);
}