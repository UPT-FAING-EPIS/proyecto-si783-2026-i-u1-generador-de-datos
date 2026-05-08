import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const ENGINE_LABELS: Record<string, string> = {
  mysql: "MySQL",
  postgresql: "PostgreSQL",
  mongodb: "MongoDB",
  redis: "Redis",
  neo4j: "Neo4j",
  cassandra: "Cassandra",
  elasticsearch: "Elasticsearch",
}

export const ENGINE_COLORS: Record<string, string> = {
  mysql: "bg-orange-100 text-orange-800",
  postgresql: "bg-blue-100 text-blue-800",
  mongodb: "bg-green-100 text-green-800",
  redis: "bg-red-100 text-red-800",
  neo4j: "bg-purple-100 text-purple-800",
  cassandra: "bg-yellow-100 text-yellow-800",
  elasticsearch: "bg-cyan-100 text-cyan-800",
}

export function formatDate(iso: string) {
  return new Date(iso).toLocaleString("es-PE", {
    dateStyle: "medium",
    timeStyle: "short",
  })
}

export function formatNumber(n: number) {
  return n.toLocaleString("es-PE")
}
