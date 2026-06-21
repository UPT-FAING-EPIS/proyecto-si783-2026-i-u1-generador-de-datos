import json
from typing import Tuple, List, Dict
from backend.models.schemas import DatabaseSchema, TableSchema, ColumnSchema

def parse_nosql_json(json_content: str) -> Tuple[DatabaseSchema, List[str]]:
    """
    Parsea un contenido JSON que representa colecciones y campos NoSQL.
    Espera un formato como:
    {
      "collection_name": {
        "field1": "string",
        "field2": "int"
      }
    }
    """
    warnings = []
    tables = []
    
    try:
        data = json.loads(json_content)
        if not isinstance(data, dict):
            raise ValueError("El JSON debe ser un objeto en la raíz.")
            
        for coll_name, fields in data.items():
            if not isinstance(fields, dict):
                warnings.append(f"La colección '{coll_name}' no tiene un formato de diccionario válido, se omite.")
                continue
                
            columns = []
            primary_keys = []
            
            # Ensure _id exists for MongoDB style or take it as it comes
            has_pk = False
            for field_name, field_type_raw in fields.items():
                if not isinstance(field_type_raw, str):
                    field_type_str = type(field_type_raw).__name__.upper()
                else:
                    field_type_str = field_type_raw.upper()
                
                is_pk = field_name == "_id"
                if is_pk:
                    has_pk = True
                    primary_keys.append(field_name)
                    
                columns.append(ColumnSchema(
                    name=field_name,
                    data_type=field_type_str,
                    is_nullable=not is_pk,
                    is_primary_key=is_pk,
                ))
            
            if not has_pk:
                columns.insert(0, ColumnSchema(
                    name="_id",
                    data_type="STRING",
                    is_nullable=False,
                    is_primary_key=True
                ))
                primary_keys.append("_id")
                warnings.append(f"Se agregó '_id' automáticamente a la colección '{coll_name}'.")

            tables.append(TableSchema(
                name=coll_name,
                columns=columns,
                primary_keys=primary_keys,
                foreign_keys=[]
            ))
            
    except Exception as e:
        raise ValueError(f"Error parseando NoSQL JSON: {str(e)}")
        
    return DatabaseSchema(
        motor="nosql_json",
        database_name="nosql_script",
        tables=tables
    ), warnings


def parse_mongodb_script(script_content: str) -> Tuple[DatabaseSchema, List[str]]:
    warnings = []
    tables = []
    
    # 1. db.createCollection con properties
    collection_matches = re.finditer(r"db\.createCollection\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*\{(.*?)\}\s*\)", script_content, re.DOTALL)
    for match in collection_matches:
        coll_name = match.group(1)
        body = match.group(2)
        
        properties_match = re.search(r"properties\s*:\s*\{([\s\S]*)\}", body)
        if properties_match:
            props_str = properties_match.group(1)
            depth = 1
            end_idx = -1
            for i, char in enumerate(props_str):
                if char == '{': depth += 1
                elif char == '}': depth -= 1
                if depth == 0:
                    end_idx = i
                    break
            
            if end_idx != -1:
                props_str = props_str[:end_idx]
            
            field_matches = re.finditer(r"['\"]?(\w+)['\"]?\s*:\s*\{[^\}]*?bsonType\s*:\s*['\"]([^'\"]+)['\"]", props_str, re.IGNORECASE | re.DOTALL)
            columns = []
            columns.append(ColumnSchema(name="_id", data_type="OBJECTID", is_nullable=False, is_primary_key=True))
            for f_match in field_matches:
                columns.append(ColumnSchema(
                    name=f_match.group(1),
                    data_type=f_match.group(2).upper(),
                    is_nullable=True,
                    is_primary_key=False
                ))
            if len(columns) > 1:
                tables.append(TableSchema(name=coll_name, columns=columns, primary_keys=["_id"], foreign_keys=[]))

    # 2. Mongoose
    mongoose_matches = re.finditer(r"(?:const|let|var)\s+(\w+)\s*=\s*new\s+(?:mongoose\.)?Schema\s*\(\s*\{([\s\S]*?)\}\s*(?:,|^\))", script_content)
    for match in mongoose_matches:
        coll_name = match.group(1)
        if coll_name.lower().endswith('schema'):
            coll_name = coll_name[:-6]
        if not coll_name.endswith('s'):
            coll_name += 's'
        
        body = match.group(2)
        columns = []
        columns.append(ColumnSchema(name="_id", data_type="OBJECTID", is_nullable=False, is_primary_key=True))
        depth = 0
        current = []
        fields_str = []
        for char in body:
            if char == '{': depth += 1
            elif char == '}': depth -= 1
            
            if char == ',' and depth == 0:
                fields_str.append("".join(current))
                current = []
            else:
                current.append(char)
        if current:
            fields_str.append("".join(current))
            
        for f_str in fields_str:
            f_str = f_str.strip()
            if not f_str: continue
            
            f_match = re.match(r"['\"]?(\w+)['\"]?\s*:\s*(.+)", f_str, re.DOTALL)
            if f_match:
                f_name = f_match.group(1)
                f_type_def = f_match.group(2).strip()
                
                f_type = "STRING"
                if f_type_def.startswith('{'):
                    type_match = re.search(r"type\s*:\s*([A-Za-z0-9_\.]+)", f_type_def)
                    if type_match:
                        f_type = type_match.group(1).split('.')[-1]
                else:
                    f_type = f_type_def.split(',')[0].strip()
                
                columns.append(ColumnSchema(
                    name=f_name,
                    data_type=f_type.upper().replace('OBJECTID', 'OBJECTID'),
                    is_nullable=True,
                    is_primary_key=False
                ))
        if len(columns) > 1:
            tables.append(TableSchema(name=coll_name.lower(), columns=columns, primary_keys=["_id"], foreign_keys=[]))
            
    if not tables:
        raise ValueError("No se encontraron colecciones válidas de MongoDB/Mongoose en el script.")
        
    return DatabaseSchema(
        motor="mongodb_script",
        database_name="mongodb_script",
        tables=tables
    ), warnings
