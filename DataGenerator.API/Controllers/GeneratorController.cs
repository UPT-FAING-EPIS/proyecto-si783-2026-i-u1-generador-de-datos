using Microsoft.AspNetCore.Mvc;
using DataGenerator.API.Models;
using DataGenerator.API.Services;
using DataGenerator.API.Exporters;
using System.Text;

namespace DataGenerator.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class GeneratorController : ControllerBase
{
    private readonly IDynamicDataGenerator _generator;
    
    public GeneratorController(IDynamicDataGenerator generator)
    {
        _generator = generator;
    }
    
 [HttpPost("generate")]
public IActionResult Generate([FromBody] DynamicTableRequest request)
{
    try
    {
        if (request.Columns == null || !request.Columns.Any())
        {
            return BadRequest(new { error = "Debes definir al menos una columna" });
        }
        
        var data = _generator.GenerateData(request);
        
        // ✅ IMPORTANTE: Verificar el valor de request.Format
        Console.WriteLine($"Formato recibido: {request.Format}");
        
        IDynamicExporter exporter = request.Format switch
        {
            OutputFormat.Sql => new SqlDynamicExporter(request.DatabaseType),
            OutputFormat.Json => new JsonDynamicExporter(),
            OutputFormat.Csv => new CsvDynamicExporter(),
            OutputFormat.MongoDb => new MongoDbExporter(),  // ← Caso MongoDB
            OutputFormat.Redis => new RedisExporter(),
            OutputFormat.Neo4j => new Neo4jExporter(),
            OutputFormat.Cassandra => new CassandraExporter(),
            _ => new JsonDynamicExporter()
        };
        
        string content = exporter.Export(data, request);
        
        // ✅ Verificar qué está generando
        Console.WriteLine($"Contenido generado (primeros 200 chars): {content.Substring(0, Math.Min(200, content.Length))}");
        
        byte[] bytes = Encoding.UTF8.GetBytes(content);
        string fileName = $"{request.TableName}_{DateTime.Now:yyyyMMdd_HHmmss}{exporter.GetFileExtension()}";
        
        return File(bytes, "application/octet-stream", fileName);
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error: {ex.Message}");
        return StatusCode(500, new { error = ex.Message });
    }
}
    [HttpGet("types")]
    public IActionResult GetAvailableTypes()
    {
        var types = Enum.GetNames(typeof(DataType))
            .Select(name => new { name, value = (int)Enum.Parse(typeof(DataType), name) })
            .ToList();
        
        return Ok(types);
    }
}