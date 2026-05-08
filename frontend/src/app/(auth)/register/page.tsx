"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { toast } from "sonner"
import { Loader2, Mail, Lock, User, Database } from "lucide-react"
import api from "@/lib/api"
import { useAuthStore } from "@/store/auth"

const schema = z.object({
  email: z.string().email("Email inválido"),
  username: z.string().min(3, "Mínimo 3 caracteres").max(30),
  full_name: z.string().optional(),
  password: z.string().min(8, "Mínimo 8 caracteres"),
  confirm_password: z.string(),
}).refine((d) => d.password === d.confirm_password, {
  message: "Las contraseñas no coinciden",
  path: ["confirm_password"],
})

type FormData = z.infer<typeof schema>

export default function RegisterPage() {
  const router = useRouter()
  const setAuth = useAuthStore((s) => s.setAuth)
  const [loading, setLoading] = useState(false)

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const { confirm_password, ...payload } = data
      const res = await api.post("/auth/register", payload)
      const user = res.data
      setAuth(user, user.access_token)
      toast.success("Cuenta creada exitosamente")
      router.push("/connections")
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Error al registrar")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-6">
        <Database className="text-blue-600" size={24} />
        <h2 className="text-xl font-semibold text-slate-800">Crear cuenta</h2>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {[
          { name: "full_name", label: "Nombre completo", type: "text", icon: User, placeholder: "Tu nombre" },
          { name: "username", label: "Username", type: "text", icon: User, placeholder: "usuario123" },
          { name: "email", label: "Email", type: "email", icon: Mail, placeholder: "tu@email.com" },
          { name: "password", label: "Contraseña", type: "password", icon: Lock, placeholder: "••••••••" },
          { name: "confirm_password", label: "Confirmar contraseña", type: "password", icon: Lock, placeholder: "••••••••" },
        ].map(({ name, label, type, icon: Icon, placeholder }) => (
          <div key={name}>
            <label className="block text-sm font-medium text-slate-700 mb-1">{label}</label>
            <div className="relative">
              <Icon className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
              <input
                {...register(name as any)}
                type={type}
                placeholder={placeholder}
                className="w-full pl-10 pr-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            {errors[name as keyof FormData] && (
              <p className="text-red-500 text-xs mt-1">{errors[name as keyof FormData]?.message}</p>
            )}
          </div>
        ))}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {loading && <Loader2 size={16} className="animate-spin" />}
          {loading ? "Creando cuenta..." : "Crear cuenta"}
        </button>
      </form>

      <p className="text-center text-sm text-slate-500 mt-6">
        ¿Ya tienes cuenta?{" "}
        <Link href="/login" className="text-blue-600 hover:underline font-medium">
          Inicia sesión
        </Link>
      </p>
    </div>
  )
}
