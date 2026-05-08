import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import ToasterProvider from "@/components/layout/ToasterProvider"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "SmartGen — Generador Inteligente de Datos",
  description: "Sistema inteligente para generar datos en bases de datos SQL y NoSQL",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className={inter.className}>
        {children}
        <ToasterProvider />
      </body>
    </html>
  )
}
