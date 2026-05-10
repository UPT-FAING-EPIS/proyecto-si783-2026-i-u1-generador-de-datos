export interface User {
  user_id: string
  email: string
  username: string
  role: "admin" | "user"
  full_name?: string
  avatar_url?: string
  access_token: string
}

export interface Connection {
  id: string
  name: string
  engine: DBEngine
  host: string
  port: number
  username?: string
  database_name?: string
  is_active: boolean
  last_used_at?: string
  created_at: string
}

export type DBEngine =
  | "mysql"
  | "postgresql"
  | "sqlserver"
  | "mongodb"
  | "redis"
  | "neo4j"
  | "cassandra"
  | "elasticsearch"

export interface ConnectionTest {
  success: boolean
  message: string
  engine_version?: string
  latency_ms?: number
}

export interface ColumnInfo {
  name: string
  data_type: string
  is_nullable: boolean
  is_primary_key: boolean
  is_unique: boolean
  is_foreign_key: boolean
  references_table?: string
  references_column?: string
  max_length?: number
}

export interface TableSchema {
  name: string
  row_count?: number
  columns: ColumnInfo[]
}

export interface SchemaAnalysis {
  engine: string
  database: string
  tables: TableSchema[]
  relationships: Record<string, string>[]
  total_tables: number
  analyzed_at: string
}

export interface TableGenerationConfig {
  table_name: string
  count: number
}

export interface GenerationRequest {
  connection_id: string
  tables: TableGenerationConfig[]
  preview_only: boolean
}

export interface InsertPreviewRequest {
  connection_id: string
  confirmed_data: Record<string, Record<string, unknown>[]>
}

export interface GenerationResult {
  table_name: string
  requested: number
  inserted: number
  errors: Record<string, unknown>[]
}

export interface GenerationPreview {
  table_name: string
  count: number
  sample: Record<string, unknown>[]
  all_data: Record<string, unknown>[]
}

export interface GenerationResponse {
  connection_id: string
  engine: string
  database: string
  results: GenerationResult[]
  previews: GenerationPreview[]
  total_inserted: number
  total_errors: number
  preview_only: boolean
}

export interface ActivityLog {
  id: string
  user_id?: string
  action: string
  detail?: string
  ip_address?: string
  created_at: string
}

export interface AdminStats {
  total_users: number
  active_users: number
  blocked_users: number
  active_sessions: number
  total_activity_logs: number
  logins_by_method: Record<string, number>
}
