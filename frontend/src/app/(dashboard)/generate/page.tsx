"use client"
import { useState, useEffect } from "react"
import { Zap, Eye, Database, Loader2, CheckCircle, AlertCircle, Info, ChevronDown, ChevronUp, Send, Download, FileJson, FileSpreadsheet, FileText, FileCode } from "lucide-react"
import { toast } from "sonner"
import api from "@/lib/api"
import { Connection, SchemaAnalysis, GenerationResponse } from "@/types"
import { ENGINE_LABELS, ENGINE_COLORS } from "@/lib/utils"

const EXPORT_FORMATS = [
  { key: "json",  label: "JSON",  icon: FileJson,        color: "text-yellow-600 hover:bg-yellow-50 border-yellow-200" },
  { key: "csv",   label: "CSV",   icon: FileText,        color: "text-green-600 hover:bg-green-50 border-green-200" },
  { key: "excel", label: "Excel", icon: FileSpreadsheet, color: "text-emerald-600 hover:bg-emerald-50 border-emerald-200" },
  { key: "sql",   label: "SQL",   icon: FileCode,        color: "text-blue-600 hover:bg-blue-50 border-blue-200" },
  { key: "xml",   label: "XML",   icon: FileText,        color: "text-orange-600 hover:bg-orange-50 border-orange-200" },
]

export default function GeneratePage() {
  const [connections, setConnections] = useState<Connection[]>([])
  const [selectedConn, setSelectedConn] = useState<string>("")
  const [schema, setSchema] = useState<SchemaAnalysis | null>(null)
  const [tableCounts, setTableCounts] = useState<Record<string, number>>({})
  const [selectedTables, setSelectedTables] = useState<Set<string>>(new Set())
  const [loadingSchema, setLoadingSchema] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [inserting, setInserting] = useState(false)
  const [exporting, setExporting] = useState<string | null>(null)
  const [preview, setPreview] = useState<GenerationResponse | null>(null)
  const [result, setResult] = useState<GenerationResponse | null>(null)
  const [expandedTables, setExpandedTables] = useState<Set<string>>(new Set())
  const [expandedResults, setExpandedResults] = useState<Set<string>>(new Set())
  const [lastInsertedData, setLastInsertedData] = useState<Record<string, any[]> | null>(null)
  const [connEngine, setConnEngine] = useState<string>("mysql")

  useEffect(() => {
    api.get("/connections/").then((r) => setConnections(r.data)).catch(() => toast.error("Error al cargar conexiones"))
  }, [])

  const handleAnalyze = async () => {
    if (!selectedConn) return toast.error("Selecciona una conexión")
    setLoadingSchema(true)
    setSchema(null)
    setPreview(null)
    setResult(null)
    setLastInsertedData(null)
    try {
      const res = await api.get(`/connections/${selectedConn}/analyze`)
      setSchema(res.data)
      setConnEngine(res.data.engine)
      const counts: Record<string, number> = {}
      const sel = new Set<string>()
      res.data.tables.forEach((t: any) => { counts[t.name] = 10; sel.add(t.name) })
      setTableCounts(counts)
      setSelectedTables(sel)
      toast.success(`${res.data.total_tables} tablas detectadas`)
    } catch { toast.error("Error al analizar esquema") }
    finally { setLoadingSchema(false) }
  }

  const handlePreview = async () => {
    if (!schema || selectedTables.size === 0) return toast.error("Selecciona al menos una tabla")
    setGenerating(true)
    setPreview(null)
    setResult(null)
    try {
      const res = await api.post("/generate/", {
        connection_id: selectedConn,
        tables: Array.from(selectedTables).map((t) => ({ table_name: t, count: tableCounts[t] || 10 })),
        preview_only: true,
      })
      setPreview(res.data)
      const total = res.data.previews.reduce((a: number, p: any) => a + p.count, 0)
      toast.info(`Vista previa lista — ${total} registros`)
    } catch (err: any) { toast.error(err.response?.data?.detail || "Error al generar vista previa") }
    finally { setGenerating(false) }
  }

  const handleInsertDirect = async () => {
    if (!schema || selectedTables.size === 0) return toast.error("Selecciona al menos una tabla")
    setGenerating(true)
    setPreview(null)
    setResult(null)
    setLastInsertedData(null)
    try {
      const res = await api.post("/generate/", {
        connection_id: selectedConn,
        tables: Array.from(selectedTables).map((t) => ({ table_name: t, count: tableCounts[t] || 10 })),
        preview_only: false,
      })
      setResult(res.data)
      const inserted: Record<string, any[]> = {}
      res.data.results.forEach((r: any) => { if (r.inserted > 0) inserted[r.table_name] = Array(r.inserted).fill({}) })
      if (res.data.total_inserted > 0) {
        toast.success(`${res.data.total_inserted} registros insertados`)
      } else {
        toast.error("No se pudieron insertar registros")
      }
    } catch (err: any) { toast.error(err.response?.data?.detail || "Error al insertar") }
    finally { setGenerating(false) }
  }

  const handleInsertFromPreview = async () => {
    if (!preview) return
    setInserting(true)
    setResult(null)
    try {
      const confirmed_data: Record<string, any[]> = {}
      preview.previews.forEach((p) => { confirmed_data[p.table_name] = p.all_data })
      const res = await api.post("/generate/insert-preview", {
        connection_id: selectedConn,
        confirmed_data,
      })
      setResult(res.data)
      setLastInsertedData(confirmed_data)
      setPreview(null)
      if (res.data.total_inserted > 0) {
        toast.success(`${res.data.total_inserted} registros insertados`)
      } else {
        toast.error("No se pudieron insertar registros")
      }
    } catch (err: any) { toast.error(err.response?.data?.detail || "Error al insertar") }
    finally { setInserting(false) }
  }

  const handleExport = async (format: string) => {
    const dataToExport = lastInsertedData || (preview ? Object.fromEntries(preview.previews.map((p) => [p.table_name, p.all_data])) : null)
    if (!dataToExport) return toast.error("No hay datos para exportar")
    setExporting(format)
    try {
      const token = localStorage.getItem("access_token")
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/export/${format}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ data: dataToExport, engine: connEngine }),
      })
      if (!res.ok) throw new Error("Error al exportar")
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `smartgen_export.${format === "excel" ? "xlsx" : format}`
      a.click()
      URL.revokeObjectURL(url)
      toast.success(`Exportado como ${format.toUpperCase()}`)
    } catch { toast.error("Error al exportar") }
    finally { setExporting(null) }
  }

  const toggleTable = (name: string) => {
    setSelectedTables((prev) => {
      const next = new Set(prev)
      next.has(name) ? next.delete(name) : next.add(name)
      return next
    })
    setPreview(null)
    setResult(null)
  }

  const getResultStatus = (item: any) => {
    if (item.inserted === item.requested) return "success"
    if (item.inserted > 0) return "partial"
    return "failed"
  }

  const getPartialReason = (item: any) => {
    const errMsg = item.errors?.[0]?.error || ""
    if (errMsg.includes("Duplicate") || errMsg.includes("unique") || errMsg.includes("UNIQUE")) return "unicidad"
    if (errMsg.includes("foreign key") || errMsg.includes("FOREIGN KEY")) return "fk"
    return "otro"
  }

  const canExport = !!lastInsertedData || !!preview
  const conn = connections.find((c) => c.id === selectedConn)

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-800">Generar Datos</h1>
        <p className="text-slate-500 text-sm mt-1">Genera datos inteligentes y pobla tus bases de datos</p>
      </div>

      {/* CONEXION */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 mb-6">
        <h2 className="font-semibold text-slate-700 mb-4">1. Selecciona una conexión</h2>
        <div className="flex gap-3">
          <select value={selectedConn} onChange={(e) => { setSelectedConn(e.target.value); setSchema(null); setPreview(null); setResult(null); setLastInsertedData(null) }}
            className="flex-1 px-3 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white">
            <option value="">— Selecciona una conexión —</option>
            {connections.map((c) => <option key={c.id} value={c.id}>{c.name} ({ENGINE_LABELS[c.engine]})</option>)}
          </select>
          <button onClick={handleAnalyze} disabled={!selectedConn || loadingSchema}
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-900 disabled:opacity-50 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition-colors">
            {loadingSchema ? <Loader2 size={16} className="animate-spin" /> : <Database size={16} />}
            Analizar
          </button>
        </div>
        {conn && (
          <div className="mt-3 flex items-center gap-2">
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${ENGINE_COLORS[conn.engine]}`}>{ENGINE_LABELS[conn.engine]}</span>
            <span className="text-xs text-slate-500">{conn.host}:{conn.port} / {conn.database_name}</span>
          </div>
        )}
      </div>

      {/* TABLAS */}
      {schema && (
        <div className="bg-white rounded-xl border border-slate-200 p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-slate-700">2. Configura las tablas</h2>
            <div className="flex gap-2">
              <button onClick={() => { setSelectedTables(new Set(schema.tables.map((t) => t.name))); setPreview(null) }} className="text-xs text-blue-600 hover:underline">Todas</button>
              <span className="text-slate-300">|</span>
              <button onClick={() => { setSelectedTables(new Set()); setPreview(null) }} className="text-xs text-slate-500 hover:underline">Ninguna</button>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4 flex items-start gap-2">
            <Info size={16} className="text-blue-500 mt-0.5 flex-shrink-0" />
            <p className="text-xs text-blue-700">
              Escribe la cantidad de registros en el campo de cada tabla. Usa <strong>Vista previa</strong> para revisar antes de insertar.
              Campos <strong>UNIQUE</strong> limitan la cantidad máxima posible.
            </p>
          </div>

          <div className="space-y-3">
            {schema.tables.map((table) => {
              const hasUnique = table.columns.some((c) => c.is_unique && !c.is_primary_key)
              const hasFK = table.columns.some((c) => c.is_foreign_key)
              return (
                <div key={table.name} className={`border rounded-lg transition-colors ${selectedTables.has(table.name) ? "border-blue-200 bg-blue-50" : "border-slate-200"}`}>
                  <div className="flex items-center gap-3 p-4">
                    <input type="checkbox" checked={selectedTables.has(table.name)} onChange={() => toggleTable(table.name)} className="w-4 h-4 text-blue-600 rounded" />
                    <div className="flex-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-medium text-slate-800 text-sm">{table.name}</span>
                        <span className="text-xs text-slate-400">({table.columns.length} cols{table.row_count !== undefined ? `, ${table.row_count} actuales` : ""})</span>
                        {hasUnique && <span className="text-xs px-1.5 py-0.5 rounded bg-purple-100 text-purple-700 font-medium">UNIQUE</span>}
                        {hasFK && <span className="text-xs px-1.5 py-0.5 rounded bg-blue-100 text-blue-700 font-medium">FK</span>}
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-2">
                        <label className="text-xs text-slate-500 whitespace-nowrap">Cant. registros:</label>
                        <input
                          type="number" min={1} max={100000}
                          value={tableCounts[table.name] || 10}
                          onChange={(e) => {
                            const val = Math.max(1, Math.min(100000, Number(e.target.value) || 1))
                            setTableCounts((p) => ({ ...p, [table.name]: val }))
                            setPreview(null)
                          }}
                          disabled={!selectedTables.has(table.name)}
                          className="w-24 px-2 py-1.5 border border-slate-300 rounded-lg text-sm text-center font-medium disabled:opacity-40 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <button onClick={() => setExpandedTables((p) => { const n = new Set(p); n.has(table.name) ? n.delete(table.name) : n.add(table.name); return n })} className="text-slate-400 hover:text-slate-600">
                        {expandedTables.has(table.name) ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                      </button>
                    </div>
                  </div>
                  {expandedTables.has(table.name) && (
                    <div className="border-t border-slate-200 p-4">
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                        {table.columns.map((col) => (
                          <div key={col.name} className="flex items-center gap-1.5 text-xs text-slate-600 bg-white rounded px-2 py-1.5 border border-slate-100">
                            <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${col.is_primary_key ? "bg-yellow-500" : col.is_foreign_key ? "bg-blue-500" : col.is_unique ? "bg-purple-500" : "bg-slate-300"}`} />
                            <span className="font-medium truncate">{col.name}</span>
                            <span className="text-slate-400 truncate">{col.data_type}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>

          <div className="flex gap-3 mt-6">
            <button onClick={handlePreview} disabled={generating || inserting || selectedTables.size === 0}
              className="flex items-center gap-2 px-5 py-2.5 border border-slate-300 rounded-lg text-sm font-medium hover:bg-slate-50 disabled:opacity-50 transition-colors">
              {generating ? <Loader2 size={16} className="animate-spin" /> : <Eye size={16} />}
              Vista previa
            </button>
            <button onClick={handleInsertDirect} disabled={generating || inserting || selectedTables.size === 0}
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition-colors">
              {generating ? <Loader2 size={16} className="animate-spin" /> : <Zap size={16} />}
              Insertar directo
            </button>
          </div>
        </div>
      )}

      {/* PREVIEW */}
      {preview && (
        <div className="bg-white rounded-xl border border-blue-200 p-6 mb-6">
          <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
            <div>
              <h2 className="font-semibold text-slate-700">3. Vista previa</h2>
              <p className="text-xs text-slate-500 mt-0.5">
                <strong>{preview.previews.reduce((a, p) => a + p.count, 0)}</strong> registros listos para insertar
              </p>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs text-slate-500 mr-1">Exportar preview:</span>
              {EXPORT_FORMATS.map(({ key, label, icon: Icon, color }) => (
                <button key={key} onClick={() => handleExport(key)} disabled={!!exporting}
                  className={`flex items-center gap-1.5 px-3 py-1.5 border rounded-lg text-xs font-medium transition-colors disabled:opacity-50 ${color}`}>
                  {exporting === key ? <Loader2 size={12} className="animate-spin" /> : <Icon size={12} />}
                  {label}
                </button>
              ))}
              <button onClick={handleInsertFromPreview} disabled={inserting}
                className="flex items-center gap-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ml-2">
                {inserting ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
                {inserting ? "Insertando..." : "Confirmar e insertar"}
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {preview.previews.map((item) => (
              <div key={item.table_name} className="border border-slate-200 rounded-lg overflow-hidden">
                <div className="flex items-center justify-between px-4 py-3 bg-slate-50">
                  <span className="font-medium text-sm text-slate-800">{item.table_name}</span>
                  <span className="text-xs text-slate-500">{item.count} registros</span>
                </div>
                {item.sample?.length > 0 && (
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead className="bg-slate-100">
                        <tr>{Object.keys(item.sample[0]).map((k) => <th key={k} className="px-3 py-2 text-left font-medium text-slate-600 whitespace-nowrap">{k}</th>)}</tr>
                      </thead>
                      <tbody>
                        {item.sample.map((row, i) => (
                          <tr key={i} className={i % 2 === 0 ? "bg-white" : "bg-slate-50"}>
                            {Object.values(row).map((v: any, j) => (
                              <td key={j} className="px-3 py-2 text-slate-700 whitespace-nowrap max-w-xs truncate">
                                {v === null ? <span className="text-slate-300 italic">null</span> : String(v)}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    {item.count > 5 && <p className="text-xs text-slate-400 text-center py-2 bg-slate-50 border-t">Mostrando 5 de {item.count} registros</p>}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* RESULTADO */}
      {result && (
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
            <h2 className="font-semibold text-slate-700">Resultado de inserción</h2>
            {lastInsertedData && (
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs text-slate-500">Exportar datos insertados:</span>
                {EXPORT_FORMATS.map(({ key, label, icon: Icon, color }) => (
                  <button key={key} onClick={() => handleExport(key)} disabled={!!exporting}
                    className={`flex items-center gap-1.5 px-3 py-1.5 border rounded-lg text-xs font-medium transition-colors disabled:opacity-50 ${color}`}>
                    {exporting === key ? <Loader2 size={12} className="animate-spin" /> : <Icon size={12} />}
                    {label}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="bg-green-50 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-green-700">{result.total_inserted}</p>
              <p className="text-xs text-green-600 mt-1">Insertados</p>
            </div>
            <div className="bg-slate-50 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-slate-700">{result.results.reduce((a, r) => a + r.requested, 0)}</p>
              <p className="text-xs text-slate-500 mt-1">Solicitados</p>
            </div>
            <div className="bg-blue-50 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-blue-700">{result.results.length}</p>
              <p className="text-xs text-blue-600 mt-1">Tablas</p>
            </div>
          </div>

          {result.total_errors > 0 && (
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 mb-4 flex items-start gap-2">
              <Info size={16} className="text-amber-500 mt-0.5 flex-shrink-0" />
              <p className="text-xs text-amber-800">Algunos registros no se insertaron por restricciones de la base de datos. Los insertados son completamente válidos.</p>
            </div>
          )}

          <div className="space-y-3">
            {result.results.map((item) => {
              const status = getResultStatus(item)
              const reason = item.errors?.length > 0 ? getPartialReason(item) : null
              return (
                <div key={item.table_name} className="border rounded-lg overflow-hidden border-slate-200">
                  <div className={`flex items-center justify-between px-4 py-3 ${status === "success" ? "bg-green-50" : status === "partial" ? "bg-amber-50" : "bg-red-50"}`}>
                    <div className="flex items-center gap-2">
                      {status === "success" && <CheckCircle size={16} className="text-green-500" />}
                      {status === "partial" && <Info size={16} className="text-amber-500" />}
                      {status === "failed" && <AlertCircle size={16} className="text-red-500" />}
                      <span className="font-medium text-sm text-slate-800">{item.table_name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-medium ${status === "success" ? "text-green-700" : status === "partial" ? "text-amber-700" : "text-red-700"}`}>
                        {item.inserted}/{item.requested} insertados
                      </span>
                      {item.errors?.length > 0 && (
                        <button onClick={() => setExpandedResults((p) => { const n = new Set(p); n.has(item.table_name) ? n.delete(item.table_name) : n.add(item.table_name); return n })} className="text-slate-400 hover:text-slate-600">
                          {expandedResults.has(item.table_name) ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                        </button>
                      )}
                    </div>
                  </div>
                  {status === "partial" && reason && (
                    <div className="px-4 py-2 bg-amber-50 border-t border-amber-100">
                      <p className="text-xs text-amber-700">
                        {reason === "unicidad" && <>Solo se insertaron <strong>{item.inserted}</strong> de <strong>{item.requested}</strong> — campo único con valores agotados.</>}
                        {reason === "fk" && <>Algunos registros no tienen referencia válida en la tabla padre.</>}
                        {reason === "otro" && <>Algunos registros no se pudieron insertar por restricciones de la base de datos.</>}
                      </p>
                    </div>
                  )}
                  {expandedResults.has(item.table_name) && item.errors?.length > 0 && (
                    <div className="border-t border-slate-200 p-3 bg-slate-50">
                      <div className="space-y-1 max-h-32 overflow-y-auto">
                        {item.errors.slice(0, 10).map((e: any, i: number) => (
                          <p key={i} className="text-xs text-slate-500 font-mono bg-white px-2 py-1 rounded border border-slate-100 truncate">Fila {e.row}: {e.error}</p>
                        ))}
                        {item.errors.length > 10 && <p className="text-xs text-slate-400 text-center">... y {item.errors.length - 10} más</p>}
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
