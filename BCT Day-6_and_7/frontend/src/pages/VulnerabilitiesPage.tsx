import React, { useState, useEffect } from 'react'
import { fetchFindings } from '@/api'
import { formatRelativeTime } from '@/utils'
import { ShieldAlert, Search, Filter } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function VulnerabilitiesPage() {
  const [findings, setFindings] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        const data = await fetchFindings(0, 100)
        if (active) setFindings(Array.isArray(data) ? data : [])
      } catch { /* ignore */ }
      finally { if (active) setLoading(false) }
    }
    load()
    const interval = setInterval(load, 30000)
    return () => { active = false; clearInterval(interval) }
  }, [])

  const severityColor = (sev: string) => {
    const s = sev?.toLowerCase()
    if (s === 'critical') return 'text-red-400 bg-red-500/10 border-red-500/30'
    if (s === 'high') return 'text-orange-400 bg-orange-500/10 border-orange-500/30'
    if (s === 'medium') return 'text-amber-400 bg-amber-500/10 border-amber-500/30'
    if (s === 'low') return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30'
    return 'text-blue-400 bg-blue-500/10 border-blue-500/30'
  }

  return (
    <div className="p-6 space-y-6 min-h-full">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <ShieldAlert className="w-6 h-6 text-red-400" /> Security Findings
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">Manage and remediate identified vulnerabilities</p>
        </div>
      </div>

      <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-800/60 bg-slate-950/50">
                {['ID', 'Severity', 'Title', 'Asset', 'Status', 'Last Seen'].map(h => (
                  <th key={h} className="text-left px-5 py-3.5 text-xs font-medium text-slate-500 uppercase tracking-wider">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading && [...Array(6)].map((_, i) => (
                <tr key={i} className="border-b border-slate-800/30">
                  <td colSpan={6} className="px-5 py-4"><div className="h-4 bg-slate-800 rounded animate-pulse" /></td>
                </tr>
              ))}
              {findings.map((f: any) => (
                <tr key={f.id} onClick={() => navigate(`/vulnerabilities/${f.id}`)} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors cursor-pointer group">
                  <td className="px-5 py-3.5 font-mono text-xs text-slate-500">#{f.id}</td>
                  <td className="px-5 py-3.5">
                    <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${severityColor(f.severity)}`}>
                      {f.severity}
                    </span>
                  </td>
                  <td className="px-5 py-3.5 text-slate-200 font-medium group-hover:text-cyan-400 transition-colors">{f.title}</td>
                  <td className="px-5 py-3.5 text-slate-400 text-xs font-mono">{f.asset?.ip_address || f.asset_id}</td>
                  <td className="px-5 py-3.5">
                    <span className={`text-xs ${f.status === 'open' ? 'text-red-400' : 'text-slate-400'}`}>{f.status}</span>
                  </td>
                  <td className="px-5 py-3.5 text-slate-500 text-xs whitespace-nowrap">{formatRelativeTime(f.last_seen)}</td>
                </tr>
              ))}
              {!loading && findings.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-5 py-16 text-center">
                    <ShieldAlert className="w-10 h-10 text-slate-700 mx-auto mb-3" />
                    <p className="text-slate-500 text-sm">No vulnerabilities found.</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
