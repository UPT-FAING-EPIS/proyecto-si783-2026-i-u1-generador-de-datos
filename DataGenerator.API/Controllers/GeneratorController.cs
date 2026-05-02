using Microsoft.AspNetCore.Mvc;
using DataGenerator.API.Models;
using DataGenerator.API.Services;
using DataGenerator.API.Factories;
using System.Text;

namespace DataGenerator.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class GeneratorController : ControllerBase
{
    private readonly IDynamicDataGenerator _generator;
    private readonly IExporterFactory _exporterFactory;

    // ✅ La Factory se inyecta, ya no hay "new" hardcodeados
    public GeneratorController(IDynamicDataGenerator generator, IExporterFactory exporterFactory)
    {
        _generator = generator;
        _exporterFactory = exporterFactory;
    }

    [HttpPost("generate")]
    public IActionResult Generate([FromBody] DynamicTableRequest request)
    {
        try
        {
            // Validación de columnas
            if (request.Columns == null || !request.Columns.Any())
                return BadRequest(new { error = "Debes definir al menos una columna" });

            // ✅ Validación de límite de registros (máx 50,000)
            if (request.RecordCount <= 0 || request.RecordCount > 50_000)
                return BadRequest(new { error = "RecordCount debe estar entre 1 y 50.000" });

            var data = _generator.GenerateData(request);

            // ✅ Factory crea el exporter correcto sin "new" en el controller
            var exporter = _exporterFactory.Create(request.Format, request.DatabaseType);
            string content = exporter.Export(data, request);

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
    // ✅ NUEVO: Preview — devuelve 5 registros en JSON para validar antes de descargar
    [HttpPost("preview")]
    public IActionResult Preview([FromBody] DynamicTableRequest request)
    {
        try
        {
            if (request.Columns == null || !request.Columns.Any())
                return BadRequest(new { error = "Debes definir al menos una columna" });

            // Siempre genera máximo 5 registros para preview
            var previewRequest = new DynamicTableRequest
            {
                TableName = request.TableName,
                RecordCount = 5,
                Format = request.Format,
                DatabaseType = request.DatabaseType,
                Columns = request.Columns
            };

            var data = _generator.GenerateData(previewRequest);

            return Ok(new
            {
                tableName = request.TableName,
                database = request.DatabaseType.ToString(),
                format = request.Format.ToString(),
                recordsShown = data.Count,
                preview = data
            });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }
}