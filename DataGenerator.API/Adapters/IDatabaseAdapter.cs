using DataGenerator.API.Models;

namespace DataGenerator.API.Adapters;

public interface IDatabaseAdapter
{
    string Name { get; }
    string GetCreateTableScript(string tableName, List<ColumnDefinition> columns);
    string GetColumnType(ColumnDefinition column);
    string FormatValue(object value, ColumnDefinition column);
    string GetInsertScript(string tableName, List<ColumnDefinition> columns, Dictionary<string, object> row);
    string GetConnectionStringExample();
}