using System.ComponentModel.DataAnnotations;

namespace DataGenerator.API.Models;

public class ColumnDefinition
{
    public string Name { get; set; } = string.Empty;
    public DataType Type { get; set; }
    public object? MinValue { get; set; }      // Para números: valor mínimo
    public object? MaxValue { get; set; }      // Para números: valor máximo
    public int? MaxLength { get; set; }        // Para strings: longitud máxima
    public List<string>? PossibleValues { get; set; }  // Para selección de valores
    public bool IsNullable { get; set; } = false;
    public object? DefaultValue { get; set; }  // Valor por defecto
    public string? Format { get; set; }        // Para fechas: "yyyy-MM-dd", etc.
}