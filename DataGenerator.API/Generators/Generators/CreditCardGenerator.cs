using Bogus;
using Bogus.DataSets;
using DataGenerator.API.Models;

namespace DataGenerator.API.Generators.Generators;

public class CreditCardGenerator : IDataGenerator
{
    public string Name => "Tarjeta de Crédito";
    public DataType DataType => DataType.CreditCardNumber;
    private readonly Faker _faker = new Faker();
    
    public object Generate(Dictionary<string, object>? options = null)
    {
        string cardType = options?.ContainsKey("cardType") == true 
                          ? options["cardType"].ToString() 
                          : null;
        
        return cardType switch
        {
            "Visa" => _faker.Finance.CreditCardNumber(CardType.Visa),
            "Mastercard" => _faker.Finance.CreditCardNumber(CardType.Mastercard),
            "American Express" => _faker.Finance.CreditCardNumber(CardType.AmericanExpress),
            _ => _faker.Finance.CreditCardNumber()
        };
    }
    
    public Dictionary<string, object> GetOptions()
    {
        return new Dictionary<string, object>
        {
            { "cardType", "Visa" },
            { "cardTypes", new[] { "Visa", "Mastercard", "American Express" } }
        };
    }
}