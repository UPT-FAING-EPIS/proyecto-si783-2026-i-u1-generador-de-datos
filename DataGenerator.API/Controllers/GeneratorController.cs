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
            // Validar que haya columnas
            if (request.Columns == null || !request.Columns.Any())
            {
                return BadRequest(new { error = "Debes definir al menos una columna" });
            }
            
            // Generar datos
            var data = _generator.GenerateData(request);
            
            // Exportar según formato
            IDynamicExporter exporter = request.Format switch
            {
                OutputFormat.Sql => new SqlDynamicExporter(request.DatabaseType),
                OutputFormat.Json => new JsonDynamicExporter(),
                OutputFormat.Csv => new CsvDynamicExporter(),
                _ => new JsonDynamicExporter()
            };
            
            string content = exporter.Export(data, request);
            byte[] bytes = Encoding.UTF8.GetBytes(content);
            
            string fileName = $"{request.TableName}_{DateTime.Now:yyyyMMdd_HHmmss}{exporter.GetFileExtension()}";
            
            return File(bytes, "application/octet-stream", fileName);
        }
        catch (Exception ex)
        {
            // ✅ Imprimir error DETALLADO en la consola
            Console.WriteLine("=========================================");
            Console.WriteLine("❌ ERROR EN GENERATE:");
            Console.WriteLine($"Mensaje: {ex.Message}");
            Console.WriteLine($"Tipo: {ex.GetType().Name}");
            Console.WriteLine($"StackTrace: {ex.StackTrace}");
            
            if (ex.InnerException != null)
            {
                Console.WriteLine("--- INNER EXCEPTION ---");
                Console.WriteLine($"Mensaje: {ex.InnerException.Message}");
                Console.WriteLine($"StackTrace: {ex.InnerException.StackTrace}");
            }
            Console.WriteLine("=========================================");
            
            // ✅ Devolver error detallado al cliente
            return StatusCode(500, new { 
                error = ex.Message,
                type = ex.GetType().Name,
                stackTrace = ex.StackTrace,
                innerError = ex.InnerException?.Message
            });
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