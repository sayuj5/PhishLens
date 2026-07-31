import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { login as apiLogin } from '@/api'

interface AuthContextType {
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null)

  useEffect(() => {
    const stored = localStorage.getItem('bf_token')
    if (stored) setToken(stored)
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    const data = await apiLogin(email, password)
    localStorage.setItem('bf_token', data.access_token)
    setToken(data.access_token)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('bf_token')
    setToken(null)
  }, [])

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
