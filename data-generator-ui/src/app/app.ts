import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

interface ColumnDefinition {
  name: string;
  type: string;
  minValue?: number;
  maxValue?: number;
  maxLength?: number;
  possibleValues?: string[];
  possibleValuesText?: string;
  isNullable: boolean;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent {
[x: string]: any;
  tableName = 'mi_tabla';
  recordCount = 100;
  outputFormat = 'Sql';
  databaseType = 'MySQL';
  columns: ColumnDefinition[] = [];
  isGenerating = false;
  message = '';
  messageType = '';

  constructor(private http: HttpClient) {
    this.addColumn();
    this.addColumn();
    this.addColumn();
    
    if (this.columns.length >= 3) {
      this.columns[0].name = 'id';
      this.columns[0].type = 'Integer';
      this.columns[0].minValue = 1;
      this.columns[0].maxValue = 10000;
      
      this.columns[1].name = 'nombre';
      this.columns[1].type = 'String';
      this.columns[1].maxLength = 50;
      
      this.columns[2].name = 'activo';
      this.columns[2].type = 'Boolean';
    }
  }

  addColumn() {
    this.columns.push({
      name: '',
      type: 'String',
      isNullable: false
    });
  }

  removeColumn(index: number) {
    this.columns.splice(index, 1);
  }

  onTypeChange(column: ColumnDefinition) {
    if (column.type !== 'Integer' && column.type !== 'Decimal') {
      column.minValue = undefined;
      column.maxValue = undefined;
    }
    if (column.type !== 'String') {
      column.maxLength = undefined;
    }
  }
generate() {
  if (!this.tableName.trim()) {
    this.message = 'El nombre de la tabla es requerido';
    this.messageType = 'error';
    setTimeout(() => this.message = '', 5000);
    return;
  }
  
  if (this.columns.length === 0) {
    this.message = 'Debes agregar al menos una columna';
    this.messageType = 'error';
    setTimeout(() => this.message = '', 5000);
    return;
  }
  
  for (let col of this.columns) {
    if (!col.name.trim()) {
      this.message = 'Todas las columnas deben tener nombre';
      this.messageType = 'error';
      setTimeout(() => this.message = '', 5000);
      return;
    }
  }
  
  // Mapeo de tipos a números
  const typeMap: { [key: string]: number } = {
    'Integer': 0,
    'Decimal': 1,
    'String': 2,
    'Boolean': 3,
    'DateTime': 4,
    'Date': 5,
    'Time': 6,
    'Guid': 7,
    'Email': 8,
    'Phone': 9,
    'Url': 10,
    'IPv4': 11,
    'IPv6': 12,
    'Enum': 13,
    'Json': 14,
    'Null': 15
  };
  
  // Mapeo de formato a número
   
  let formatValue = 0;
  switch (this.outputFormat) {
    case 'Sql': formatValue = 0; break;
    case 'Json': formatValue = 1; break;
    case 'Csv': formatValue = 2; break;
  }
  
  let dbTypeValue = 0;
  switch (this.databaseType) {
    case 'MySQL': dbTypeValue = 0; break;
    case 'PostgreSQL': dbTypeValue = 1; break;
    case 'MicrosoftSQLServer': dbTypeValue = 2; break;
  }
  
  // ✅ ESTRUCTURA CORRECTA - SIN "request" envolviendo
  const requestData = {
    TableName: this.tableName,
    RecordCount: this.recordCount,
    Format: formatValue,
    DatabaseType: dbTypeValue,
    Columns: this.columns.map(col => {
      const processedCol: any = {
        Name: col.name,
        Type: this.getTypeValue(col.type),
        IsNullable: col.isNullable
      };
      
      if (col.minValue !== undefined && col.minValue !== null) {
        processedCol.MinValue = Number(col.minValue);
      }
      if (col.maxValue !== undefined && col.maxValue !== null) {
        processedCol.MaxValue = Number(col.maxValue);
      }
      if (col.maxLength !== undefined && col.maxLength !== null && col.type === 'String') {
        processedCol.MaxLength = Number(col.maxLength);
      }
      
      if (col.type === 'Enum' && col.possibleValuesText) {
        processedCol.PossibleValues = col.possibleValuesText.split(',').map(v => v.trim());
      }
      
      return processedCol;
    })
  };
  
  console.log('Enviando:', JSON.stringify(requestData, null, 2));
  
  this.isGenerating = true;
  this.message = 'Generando datos...';
  this.messageType = 'info';
  
  this.http.post('http://localhost:5000/api/generator/generate', requestData, {
    responseType: 'blob'
  }).subscribe({
    next: (blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const extension = this.outputFormat === 'Sql' ? 'sql' : this.outputFormat.toLowerCase();
      a.download = `${this.tableName}_${Date.now()}.${extension}`;
      a.click();
      window.URL.revokeObjectURL(url);
      
      this.message = '✅ Archivo generado correctamente';
      this.messageType = 'success';
      this.isGenerating = false;
      setTimeout(() => this.message = '', 5000);
    },
    error: (err) => {
      console.error('Error:', err);
      this.message = '❌ Error al generar';
      this.messageType = 'error';
      this.isGenerating = false;
      setTimeout(() => this.message = '', 5000);
    }
  });
}

getTypeValue(typeName: string): number {
  const typeMap: { [key: string]: number } = {
    // Tipos básicos (0-7)
    'Integer': 0,
    'Decimal': 1,
    'String': 2,
    'Boolean': 3,
    'DateTime': 4,
    'Date': 5,
    'Time': 6,
    'Guid': 7,
    
    // Persona (8-11)
    'FullName': 8,
    'FirstName': 9,
    'LastName': 10,
    'UserName': 11,
    
    // Contacto (12-14)
    'Email': 12,
    'Phone': 13,
    'CellPhone': 14,
    
    // Ubicación (15-20)
    'City': 15,
    'Country': 16,
    'Address': 17,
    'ZipCode': 18,
    'Latitude': 19,
    'Longitude': 20,
    
    // Internet (21-24)
    'IPv4': 21,
    'IPv6': 22,
    'Url': 23,
    'DomainName': 24,
    
    // Finanzas (25-29)
    'CreditCardNumber': 25,
    'CreditCardType': 26,
    'Amount': 27,
    'Currency': 28,
    'IBAN': 29,
    
    // Empresa (30-32)
    'CompanyName': 30,
    'JobTitle': 31,
    'Department': 32,
    
    // Producto (33-36)
    'ProductName': 33,
    'ProductDescription': 34,
    'Price': 35,
    'SKU': 36,
    
    // Texto (37-40)
    'Text': 37,
    'Paragraph': 38,
    'Sentence': 39,
    'Word': 40,
    
    // Identificadores (41-44)
    'UUID': 41,
    'Cuit': 42,
    'Rfc': 43,
    'Dni': 44,
    
    // Otros (45-50)
    'Color': 45,
    'ImageUrl': 46,
    'DateRange': 47,
    'Enum': 48,
    'Json': 49,
    'Null': 50
  };
  
  return typeMap[typeName] ?? 2; // Por defecto String (2)
}
}