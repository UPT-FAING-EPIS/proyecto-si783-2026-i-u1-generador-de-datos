"use client"
import { useState, useEffect } from "react"
import { Plus, Database, Trash2, Search, Zap, CheckCircle, XCircle, Loader2 } from "lucide-react"
import { toast } from "sonner"
import api from "@/lib/api"
import { Connection, ConnectionTest, DBEngine } from "@/types"
import { ENGINE_COLORS, ENGINE_LABELS, formatDate } from "@/lib/utils"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const schema = z.object({
  name: z.string().min(1, "Nombre requerido"),
  engine: z.enum(["mysql","postgresql","mongodb","redis","neo4j","cassandra","elasticsearch"]),
  host: z.string().min(1, "Host requerido"),
  port: z.coerce.number().min(1).max(65535),
  username: z.string().optional(),
  password: z.string().optional(),
  database_name: z.string().optional(),
})

type FormData = z.infer<typeof schema>

const DEFAULT_PORTS: Record<string, number> = {
  mysql: 3306, postgresql: 5432, mongodb: 27017,
  redis: 6379, neo4j: 7687, cassandra: 9042, elasticsearch: 9200,
}

export default function ConnectionsPage() {
  const [connections, setConnections] = useState<Connection[]>([])
  const [showModal, setShowModal] = useState(false)
  const [testing, setTesting] = useState(false)
  const [saving, setSaving] = useState(false)
  const [testResult, setTestResult] = useState<ConnectionTest | null>(null)
  const [loading, setLoading] = useState(true)

  const { register, handleSubmit, watch, setValue, reset, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema as any),
    defaultValues: { engine: "mysql", host: "localhost", port: 3306 },
  })

  const engine = watch("engine")

  useEffect(() => {
    setValue("port", DEFAULT_PORTS[engine] || 3306)
    setTestResult(null)
  }, [engine, setValue])

  useEffect(() => { fetchConnections() }, [])

  const fetchConnections = async () => {
    try {
      const res = await api.get("/connections/")
      setConnections(res.data)
    } catch { toast.error("Error al cargar conexiones") }
    finally { setLoading(false) }
  }

  const handleTest = async (data: FormData) => {
    setTesting(true)
    setTestResult(null)
    try {
      const res = await api.post("/connections/test", data)
      setTestResult(res.data)
      if (res.data.success) toast.success("Conexión exitosa")
      else toast.error("Conexión fallida")
    } catch { toast.error("Error al probar conexión") }
    finally { setTesting(false) }
  }

  const handleSave = async (data: FormData) => {
    setSaving(true)
    try {
      await api.post("/connections/", data)
      toast.success("Conexión guardada")
      setShowModal(false)
      reset()
      setTestResult(null)
      fetchConnections()
    } catch (err: any) { toast.error(err.response?.data?.detail || "Error al guardar") }
    finally { setSaving(false) }
  }

  const handleDelete = async (id: string) => {
    if (!confirm("¿Eliminar esta conexión?")) return
    try {
      await api.delete(`/connections/${id}`)
      toast.success("Conexión eliminada")
      fetchConnections()
    } catch { toast.error("Error al eliminar") }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Conexiones</h1>
          <p className="text-slate-500 text-sm mt-1">Gestiona tus conexiones a bases de datos</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg text-sm font-medium transition-colors"
        >
          <Plus size={16} /> Nueva conexión
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-40">
          <Loader2 className="animate-spin text-blue-600" size={32} />
        </div>
      ) : connections.length === 0 ? (
        <div className="text-center py-20 text-slate-400">
          <Database size={48} className="mx-auto mb-4 opacity-30" />
          <p className="font-medium">No tienes conexiones guardadas</p>
          <p className="text-sm mt-1">Crea tu primera conexión para comenzar</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {connections.map((conn) => (
            <div key={conn.id} className="bg-white rounded-xl border border-slate-200 p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-slate-800">{conn.name}</h3>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium mt-1 inline-block ${ENGINE_COLORS[conn.engine]}`}>
                    {ENGINE_LABELS[conn.engine]}
                  </span>
                </div>
                <button onClick={() => handleDelete(conn.id)} className="text-slate-400 hover:text-red-500 transition-colors">
                  <Trash2 size={16} />
                </button>
              </div>
              <div className="text-xs text-slate-500 space-y-1">
                <p><span className="font-medium">Host:</span> {conn.host}:{conn.port}</p>
                {conn.database_name && <p><span className="font-medium">BD:</span> {conn.database_name}</p>}
                {conn.last_used_at && <p><span className="font-medium">Último uso:</span> {formatDate(conn.last_used_at)}</p>}
              </div>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b">
              <h2 className="text-lg font-semibold text-slate-800">Nueva conexión</h2>
            </div>
            <form className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Nombre</label>
                  <input {...register("name")} placeholder="Mi base de datos" className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>}
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Motor</label>
                  <select {...register("engine")} className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white">
                    {Object.entries(ENGINE_LABELS).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Host</label>
                  <input {...register("host")} placeholder="localhost" className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Puerto</label>
                  <input {...register("port")} type="number" className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Usuario</label>
                  <input {...register("username")} placeholder="root" className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
                  <input {...register("password")} type="password" placeholder="••••••••" className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Base de datos</label>
                  <input {...register("database_name")} placeholder="nombre_bd" className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
              </div>

              {testResult && (
                <div className={`flex items-center gap-2 p-3 rounded-lg text-sm ${testResult.success ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>
                  {testResult.success ? <CheckCircle size={16} /> : <XCircle size={16} />}
                  <span>{testResult.success ? `${testResult.engine_version} — ${testResult.latency_ms}ms` : testResult.message}</span>
                </div>
              )}

              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => { setShowModal(false); reset(); setTestResult(null) }} className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors">
                  Cancelar
                </button>
                <button type="button" onClick={handleSubmit(handleTest)} disabled={testing} className="flex items-center gap-2 px-4 py-2.5 border border-blue-300 text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-50 transition-colors disabled:opacity-50">
                  {testing ? <Loader2 size={14} className="animate-spin" /> : <Search size={14} />}
                  Probar
                </button>
                <button type="button" onClick={handleSubmit(handleSave)} disabled={saving} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-4 py-2.5 rounded-lg text-sm font-medium transition-colors">
                  {saving ? <Loader2 size={14} className="animate-spin" /> : <Plus size={14} />}
                  Guardar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
