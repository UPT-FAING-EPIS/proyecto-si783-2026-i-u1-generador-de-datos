using DataGenerator.API.Services;
using DataGenerator.API.Factories;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Servicios
builder.Services.AddScoped<IDynamicDataGenerator, DynamicDataGenerator>();

// Factory de exporters (reemplaza los "new" del controller)
builder.Services.AddSingleton<IExporterFactory, ExporterFactory>();

var app = builder.Build();

app.UseCors(policy => policy.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());
app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();

app.Run();