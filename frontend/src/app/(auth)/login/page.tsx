"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { toast } from "sonner"
import { Loader2, Mail, Lock, Database } from "lucide-react"
import api from "@/lib/api"
import { useAuthStore } from "@/store/auth"

const schema = z.object({
  email: z.string().email("Email inválido"),
  password: z.string().min(1, "Ingresa tu contraseña"),
})

type FormData = z.infer<typeof schema>

export default function LoginPage() {
  const router = useRouter()
  const setAuth = useAuthStore((s) => s.setAuth)
  const [loading, setLoading] = useState(false)

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const res = await api.post("/auth/login", data)
      const user = res.data
      setAuth(user, user.access_token)
      toast.success(`Bienvenido, ${user.username}`)
      router.push("/connections")
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Credenciales incorrectas")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-6">
        <Database className="text-blue-600" size={24} />
        <h2 className="text-xl font-semibold text-slate-800">Iniciar sesión</h2>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            <input
              {...register("email")}
              type="email"
              placeholder="tu@email.com"
              className="w-full pl-10 pr-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            <input
              {...register("password")}
              type="password"
              placeholder="••••••••"
              className="w-full pl-10 pr-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {loading && <Loader2 size={16} className="animate-spin" />}
          {loading ? "Ingresando..." : "Ingresar"}
        </button>
      </form>

      <p className="text-center text-sm text-slate-500 mt-6">
        ¿No tienes cuenta?{" "}
        <Link href="/register" className="text-blue-600 hover:underline font-medium">
          Regístrate
        </Link>
      </p>
    </div>
  )
}
