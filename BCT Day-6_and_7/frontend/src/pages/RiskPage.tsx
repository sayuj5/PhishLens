import React, { useState, useEffect } from 'react'
import { fetchRiskSummary } from '@/api'
import { TrendingUp, AlertTriangle } from 'lucide-react'
import { ProgressBar } from '@/components/ui/ProgressBar'

export default function RiskPage() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRiskSummary().then(res => setData(Array.isArray(res) ? res : [])).finally(() => setLoading(false))
  }, [])

  return (
    <div className="p-6 space-y-6 min-h-full">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <TrendingUp className="w-6 h-6 text-amber-400" /> Risk Analytics
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">Asset risk scores based on active vulnerabilities</p>
        </div>
      </div>

      <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 p-5 overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="bg-slate-950/50 border-b border-slate-800/60">
            <tr>
              <th className="px-5 py-3 text-xs font-medium text-slate-500 uppercase">Asset</th>
              <th className="px-5 py-3 text-xs font-medium text-slate-500 uppercase">Risk Score (0-100)</th>
              <th className="px-5 py-3 text-xs font-medium text-slate-500 uppercase text-center">Critical</th>
              <th className="px-5 py-3 text-xs font-medium text-slate-500 uppercase text-center">High</th>
            </tr>
          </thead>
          <tbody>
            {loading && <tr><td colSpan={4} className="px-5 py-8 text-center text-slate-500">Loading risk data…</td></tr>}
            {data.map(r => (
              <tr key={r.asset_id} className="border-b border-slate-800/30">
                <td className="px-5 py-3 font-mono text-xs text-slate-300">{r.ip_address}</td>
                <td className="px-5 py-3"><ProgressBar value={r.risk_score} color={r.risk_score > 70 ? 'red' : r.risk_score > 40 ? 'amber' : 'emerald'} showLabel /></td>
                <td className="px-5 py-3 text-center text-red-400 font-bold">{r.critical}</td>
                <td className="px-5 py-3 text-center text-orange-400 font-bold">{r.high}</td>
              </tr>
            ))}
            {!loading && data.length === 0 && (
              <tr><td colSpan={4} className="px-5 py-16 text-center text-slate-500"><AlertTriangle className="w-8 h-8 mx-auto mb-2 opacity-50"/>No risk data available. Run assessments first.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
