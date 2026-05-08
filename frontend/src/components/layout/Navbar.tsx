"use client"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { Database, Zap, Shield, LogOut, User } from "lucide-react"
import { useAuthStore } from "@/store/auth"
import { cn } from "@/lib/utils"
import { toast } from "sonner"
import api from "@/lib/api"

const navItems = [
  { href: "/connections", label: "Conexiones", icon: Database },
  { href: "/generate", label: "Generar", icon: Zap },
]

export default function Navbar() {
  const pathname = usePathname()
  const router = useRouter()
  const { user, logout, isAdmin } = useAuthStore()

  const handleLogout = async () => {
    try { await api.post("/auth/logout") } catch {}
    logout()
    toast.success("Sesión cerrada")
    router.push("/login")
  }

  return (
    <nav className="bg-slate-900 text-white h-screen w-64 flex flex-col fixed left-0 top-0 z-50">
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center gap-2">
          <Database size={24} className="text-blue-400" />
          <span className="text-lg font-bold">SmartGen</span>
        </div>
        <p className="text-xs text-slate-400 mt-1">Generador de Datos</p>
      </div>

      <div className="flex-1 p-4 space-y-1">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={cn(
              "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
              pathname.startsWith(href)
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-800 hover:text-white"
            )}
          >
            <Icon size={18} />
            {label}
          </Link>
        ))}

        {isAdmin() && (
          <Link
            href="/admin"
            className={cn(
              "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
              pathname.startsWith("/admin")
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-800 hover:text-white"
            )}
          >
            <Shield size={18} />
            Administración
          </Link>
        )}
      </div>

      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center gap-3 mb-3 px-2">
          <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-xs font-bold">
            {user?.username?.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.username}</p>
            <p className="text-xs text-slate-400 capitalize">{user?.role}</p>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm text-slate-300 hover:bg-red-600 hover:text-white transition-colors"
        >
          <LogOut size={16} />
          Cerrar sesión
        </button>
      </div>
    </nav>
  )
}
