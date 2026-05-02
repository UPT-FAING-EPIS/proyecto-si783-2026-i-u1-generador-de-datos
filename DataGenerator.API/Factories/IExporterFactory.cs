// Factories/IExporterFactory.cs
using DataGenerator.API.Exporters;
using DataGenerator.API.Models;

namespace DataGenerator.API.Factories;

public interface IExporterFactory
{
    IDynamicExporter Create(OutputFormat format, DatabaseType databaseType);
}