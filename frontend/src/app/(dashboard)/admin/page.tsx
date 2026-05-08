"use client"
import { useState, useEffect } from "react"
import { Users, Activity, BarChart3, Shield, Loader2, UserX, UserCheck } from "lucide-react"
import { toast } from "sonner"
import api from "@/lib/api"
import { AdminStats, ActivityLog } from "@/types"
import { formatDate } from "@/lib/utils"

export default function AdminPage() {
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [logs, setLogs] = useState<ActivityLog[]>([])
  const [users, setUsers] = useState<any[]>([])
  const [tab, setTab] = useState<"stats" | "users" | "logs">("stats")
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchAll() }, [])

  const fetchAll = async () => {
    setLoading(true)
    try {
      const [s, l, u] = await Promise.all([
        api.get("/admin/stats"),
        api.get("/admin/logs?limit=50"),
        api.get("/admin/users"),
      ])
      setStats(s.data)
      setLogs(l.data)
      setUsers(u.data)
    } catch { toast.error("Error al cargar datos de administración") }
    finally { setLoading(false) }
  }

  const handleBlock = async (id: string, blocked: boolean) => {
    try {
      await api.post(`/admin/users/${id}/${blocked ? "unblock" : "block"}`)
      toast.success(blocked ? "Usuario desbloqueado" : "Usuario bloqueado")
      fetchAll()
    } catch { toast.error("Error al actualizar usuario") }
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="animate-spin text-blue-600" size={32} />
    </div>
  )

  return (
    <div>
      <div className="flex items-center gap-3 mb-8">
        <Shield className="text-blue-600" size={28} />
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Administración</h1>
          <p className="text-slate-500 text-sm mt-1">Panel de control del sistema</p>
        </div>
      </div>

      <div className="flex gap-2 mb-6 border-b border-slate-200">
        {[
          { key: "stats", label: "Estadísticas", icon: BarChart3 },
          { key: "users", label: "Usuarios", icon: Users },
          { key: "logs", label: "Actividad", icon: Activity },
        ].map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => setTab(key as any)}
            className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors -mb-px ${tab === key ? "border-blue-600 text-blue-600" : "border-transparent text-slate-500 hover:text-slate-700"}`}
          >
            <Icon size={16} /> {label}
          </button>
        ))}
      </div>

      {tab === "stats" && stats && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Total usuarios", value: stats.total_users, color: "blue" },
              { label: "Usuarios activos", value: stats.active_users, color: "green" },
              { label: "Bloqueados", value: stats.blocked_users, color: "red" },
              { label: "Sesiones activas", value: stats.active_sessions, color: "purple" },
            ].map(({ label, value, color }) => (
              <div key={label} className={`bg-${color}-50 rounded-xl p-5 text-center`}>
                <p className={`text-3xl font-bold text-${color}-700`}>{value}</p>
                <p className={`text-xs text-${color}-600 mt-1`}>{label}</p>
              </div>
            ))}
          </div>

          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h3 className="font-semibold text-slate-700 mb-4">Métodos de login</h3>
            <div className="space-y-3">
              {Object.entries(stats.logins_by_method).map(([method, count]) => (
                <div key={method} className="flex items-center gap-3">
                  <span className="text-sm font-medium text-slate-700 w-24 capitalize">{method}</span>
                  <div className="flex-1 bg-slate-100 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{ width: `${Math.min((count / Math.max(...Object.values(stats.logins_by_method))) * 100, 100)}%` }}
                    />
                  </div>
                  <span className="text-sm text-slate-500 w-8 text-right">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {tab === "users" && (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                {["Usuario", "Email", "Rol", "Estado", "Registro", "Acciones"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-800">{u.username}</td>
                  <td className="px-4 py-3 text-slate-500">{u.email}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${u.role === "admin" ? "bg-purple-100 text-purple-800" : "bg-slate-100 text-slate-700"}`}>{u.role}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${u.is_active ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
                      {u.is_active ? "Activo" : "Bloqueado"}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-500 text-xs">{formatDate(u.created_at)}</td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => handleBlock(u.id, !u.is_active)}
                      className={`flex items-center gap-1 text-xs px-2 py-1 rounded transition-colors ${u.is_active ? "text-red-600 hover:bg-red-50" : "text-green-600 hover:bg-green-50"}`}
                    >
                      {u.is_active ? <><UserX size={12} /> Bloquear</> : <><UserCheck size={12} /> Desbloquear</>}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === "logs" && (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                {["Acción", "Detalle", "IP", "Fecha"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <span className="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 font-medium">{log.action}</span>
                  </td>
                  <td className="px-4 py-3 text-slate-500 max-w-xs truncate">{log.detail || "—"}</td>
                  <td className="px-4 py-3 text-slate-500 font-mono text-xs">{log.ip_address || "—"}</td>
                  <td className="px-4 py-3 text-slate-500 text-xs">{formatDate(log.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
