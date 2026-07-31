import React, { useState, useEffect } from 'react'
import { HeartPulse } from 'lucide-react'

export default function HealthPage() {
  const [health, setHealth] = useState<any>(null)
  useEffect(() => {
    fetch('/health').then(r => r.json()).then(setHealth).catch(() => {})
  }, [])
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white flex items-center gap-2.5 mb-6">
        <HeartPulse className="w-6 h-6 text-emerald-400" /> System Health
      </h1>
      {health ? (
        <pre className="p-4 bg-slate-900 border border-slate-800 rounded-lg text-sm text-cyan-400">{JSON.stringify(health, null, 2)}</pre>
      ) : <p className="text-slate-500">Checking health…</p>}
    </div>
  )
}
