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

  selectDatabase(db: string) {
  this.databaseType = db;

  const formatMap: { [key: string]: string } = {
    'MySQL': 'Sql', 'PostgreSQL': 'Sql',
    'MicrosoftSQLServer': 'Sql', 'Oracle': 'Sql',
    'MongoDB': 'MongoDb',
    'Redis': 'Redis',
    'DynamoDB': 'DynamoDb',
    'Elasticsearch': 'Elasticsearch',
    'Neo4j': 'Neo4j',
    'Cassandra': 'Cassandra',
    'InfluxDB': 'InfluxDb'
  };
  this.outputFormat = formatMap[db] || 'Sql';
}

  getOutputFormatLabel(): string {
  const formatMap: { [key: string]: string } = {
    'MySQL': 'SQL (MySQL)', 'PostgreSQL': 'SQL (PostgreSQL)',
    'MicrosoftSQLServer': 'SQL (SQL Server)', 'Oracle': 'SQL (Oracle)',
    'MongoDB': 'JSON (mongosh)', 'Redis': 'Redis CLI',
    'DynamoDB': 'AWS CLI (PutItem)', 'Elasticsearch': 'ES JSON + REST',
    'Neo4j': 'Cypher', 'Cassandra': 'CQL', 'InfluxDB': 'Line Protocol'
  };
  return formatMap[this.databaseType] || 'SQL';
}

  getFileExtension(): string {
  const extMap: { [key: string]: string } = {
    'MySQL': 'sql', 'PostgreSQL': 'sql',
    'MicrosoftSQLServer': 'sql', 'Oracle': 'sql',
    'MongoDB': 'json', 'Redis': 'redis',
    'DynamoDB': 'json', 'Elasticsearch': 'json',
    'Neo4j': 'cypher', 'Cassandra': 'cql', 'InfluxDB': 'lp'
  };
  return extMap[this.databaseType] || 'txt';
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
    
    return typeMap[typeName] ?? 2;
  }
  
getFormatValue(format: string): number {
  const formats: { [key: string]: number } = {
    'Sql': 0, 'Json': 1, 'Csv': 2, 'MongoDb': 3, 'Redis': 4,
    'Neo4j': 5, 'Cassandra': 6, 'Elasticsearch': 7, 'InfluxDb': 8, 'DynamoDb': 9
  };
  return formats[format] ?? 0;
}
  getDatabaseTypeValue(db: string): number {
  const databases: { [key: string]: number } = {
    'MySQL': 0, 'PostgreSQL': 1, 'MicrosoftSQLServer': 2, 'Oracle': 3,
    'MongoDB': 10, 'Redis': 11, 'DynamoDB': 12,
    'Elasticsearch': 13, 'Neo4j': 14, 'Cassandra': 15, 'InfluxDB': 16
  };
  return databases[db] ?? 0;
}

  generate() {
    // Validaciones
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
    
    // Determinar outputFormat según la base de datos seleccionada
    let outputFormat = 'Sql';
    const formatMap: { [key: string]: string } = {
  'MySQL': 'Sql', 'PostgreSQL': 'Sql',
  'MicrosoftSQLServer': 'Sql', 'Oracle': 'Sql',
  'MongoDB': 'MongoDb', 'Redis': 'Redis',
  'DynamoDB': 'DynamoDb', 'Elasticsearch': 'Elasticsearch',
  'Neo4j': 'Neo4j', 'Cassandra': 'Cassandra', 'InfluxDB': 'InfluxDb'
};
    outputFormat = formatMap[this.databaseType] || 'Sql';
    
    // Construir request
    const requestData = {
      TableName: this.tableName,
      RecordCount: this.recordCount,
      Format: this.getFormatValue(outputFormat),
      DatabaseType: this.getDatabaseTypeValue(this.databaseType),
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
        
        // Usar la extensión según la base de datos
        const extension = this.getFileExtension();
        a.download = `${this.tableName}_${Date.now()}.${extension}`;
        a.click();
        window.URL.revokeObjectURL(url);
        
        this.message = `✅ Archivo generado correctamente (${extension})`;
        this.messageType = 'success';
        this.isGenerating = false;
        setTimeout(() => this.message = '', 5000);
      },
      error: (err) => {
        console.error('Error:', err);
        this.message = '❌ Error al generar los datos';
        this.messageType = 'error';
        this.isGenerating = false;
        setTimeout(() => this.message = '', 5000);
      }
    });

    
  }
  // ===== TEMPLATES DE DOMINIO =====
readonly templates: { [key: string]: { label: string; icon: string; columns: any[] } } = {
  ecommerce: {
    label: 'E-Commerce',
    icon: '🛒',
    columns: [
      { name: 'product_id',    type: 'Guid',               isNullable: false },
      { name: 'product_name',  type: 'ProductName',        isNullable: false },
      { name: 'description',   type: 'ProductDescription', isNullable: true  },
      { name: 'price',         type: 'Price',              isNullable: false },
      { name: 'sku',           type: 'SKU',                isNullable: false },
      { name: 'stock',         type: 'Integer',            isNullable: false, minValue: 0, maxValue: 500 },
      { name: 'category',      type: 'Department',         isNullable: false },
      { name: 'image_url',     type: 'ImageUrl',           isNullable: true  },
    ]
  },
  banking: {
    label: 'Bancario',
    icon: '🏦',
    columns: [
      { name: 'account_id',    type: 'Guid',              isNullable: false },
      { name: 'full_name',     type: 'FullName',          isNullable: false },
      { name: 'email',         type: 'Email',             isNullable: false },
      { name: 'iban',          type: 'IBAN',              isNullable: false },
      { name: 'card_number',   type: 'CreditCardNumber',  isNullable: false },
      { name: 'balance',       type: 'Amount',            isNullable: false },
      { name: 'currency',      type: 'Currency',          isNullable: false },
      { name: 'created_at',    type: 'DateTime',          isNullable: false },
    ]
  },
  users: {
    label: 'Usuarios',
    icon: '👤',
    columns: [
      { name: 'user_id',       type: 'Guid',      isNullable: false },
      { name: 'username',      type: 'UserName',  isNullable: false },
      { name: 'full_name',     type: 'FullName',  isNullable: false },
      { name: 'email',         type: 'Email',     isNullable: false },
      { name: 'phone',         type: 'Phone',     isNullable: true  },
      { name: 'city',          type: 'City',      isNullable: false },
      { name: 'country',       type: 'Country',   isNullable: false },
      { name: 'created_at',    type: 'DateTime',  isNullable: false },
    ]
  },
  iot: {
    label: 'IoT / Sensores',
    icon: '📡',
    columns: [
      { name: 'device_id',     type: 'Guid',      isNullable: false },
      { name: 'ip_address',    type: 'IPv4',      isNullable: false },
      { name: 'latitude',      type: 'Latitude',  isNullable: false },
      { name: 'longitude',     type: 'Longitude', isNullable: false },
      { name: 'timestamp',     type: 'DateTime',  isNullable: false },
      { name: 'temperature',   type: 'Decimal',   isNullable: false, minValue: -20, maxValue: 80 },
      { name: 'is_online',     type: 'Boolean',   isNullable: false },
    ]
  }
};

// Método para cargar un template
loadTemplate(key: string) {
  const template = this.templates[key];
  if (!template) return;

  this.columns = template.columns.map(col => ({
    name: col.name,
    type: col.type,
    isNullable: col.isNullable ?? false,
    minValue: col.minValue ?? null,
    maxValue: col.maxValue ?? null,
    maxLength: undefined,
    possibleValuesText: ''
  }));

  this.message = `✅ Template "${template.label}" cargado con ${this.columns.length} columnas`;
  this.messageType = 'success';
  setTimeout(() => this.message = '', 4000);
}

}
