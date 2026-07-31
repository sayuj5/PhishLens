import React, { Suspense } from 'react'
import { AuthProvider } from '@/contexts/AuthContext'
import AppRoutes from '@/routes'

export default function App() {
  return (
    <AuthProvider>
      <Suspense fallback={
        <div className="flex h-screen items-center justify-center bg-[#080c14]">
          <div className="text-slate-400 text-sm animate-pulse">Loading…</div>
        </div>
      }>
        <AppRoutes />
      </Suspense>
    </AuthProvider>
  )
}
