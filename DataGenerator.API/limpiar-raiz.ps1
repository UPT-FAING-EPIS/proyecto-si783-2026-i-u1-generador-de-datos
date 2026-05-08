# Eliminar archivos duplicados en la raiz del proyecto
# Los originales estan en subcarpetas (Models/, Controllers/, Exporters/)

$ErrorActionPreference = "Stop"

Write-Host "Eliminando duplicados en la raiz..." -ForegroundColor Red
Write-Host ""

$duplicados = @(
    "Neo4jExporter.cs",
    "SqlDynamicExporter.cs",
    "GeneratorController.cs",
    "ColumnDefinition.cs"
)

foreach ($archivo in $duplicados) {
    if (Test-Path $archivo) {
        Remove-Item $archivo -Force
        Write-Host "  ELIMINADO (raiz): $archivo" -ForegroundColor Red
    } else {
        Write-Host "  NO EXISTE: $archivo" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Compilando..." -ForegroundColor Yellow
Write-Host ""

dotnet build

Write-Host ""
Write-Host "Listo." -ForegroundColor Cyan
