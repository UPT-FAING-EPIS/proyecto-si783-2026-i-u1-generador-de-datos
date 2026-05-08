"use client"
import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuthStore } from "@/store/auth"
import Navbar from "@/components/layout/Navbar"

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const { user } = useAuthStore()

  useEffect(() => {
    if (!user) router.push("/login")
  }, [user, router])

  if (!user) return null

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Navbar />
      <main className="flex-1 ml-64 p-8">
        {children}
      </main>
    </div>
  )
}
