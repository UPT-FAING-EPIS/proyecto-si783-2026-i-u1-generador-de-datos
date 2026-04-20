using DataGenerator.API.Services;
using DataGenerator.API.Generators;
using DataGenerator.API.Generators.Generators;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Registrar servicios
builder.Services.AddScoped<IDynamicDataGenerator, DynamicDataGenerator>();

// Registrar todos los generadores semánticos
builder.Services.AddSingleton<FullNameGenerator>();
builder.Services.AddSingleton<EmailGenerator>();
builder.Services.AddSingleton<CityGenerator>();
builder.Services.AddSingleton<CreditCardGenerator>();

var app = builder.Build();

app.UseCors(policy => policy.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());
app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();

app.Run();