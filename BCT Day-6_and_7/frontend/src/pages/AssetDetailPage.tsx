import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { fetchAsset } from '@/api'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { formatRelativeTime, formatDate } from '@/utils'
import { Server, ArrowLeft, Network, HardDrive, Clock, Fingerprint } from 'lucide-react'

export default function AssetDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [asset, setAsset] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let active = true
    if (!id) return
    const load = async () => {
      try {
        const data = await fetchAsset(Number(id))
        if (active) setAsset(data)
      } catch { /* ignore */ }
      finally { if (active) setIsLoading(false) }
    }
    load()
    const interval = setInterval(load, 30000)
    return () => { active = false; clearInterval(interval) }
  }, [id])

  if (isLoading) return <div className="p-6 text-slate-500 animate-pulse">Loading asset…</div>
  if (!asset) return <div className="p-6 text-red-400">Asset not found</div>

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto">
      <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back
      </button>

      <div className="flex items-start justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center shadow-lg shadow-cyan-500/10">
            <Server className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">{asset.hostname || asset.ip_address}</h1>
            <p className="text-sm text-slate-500 font-mono mt-0.5">{asset.ip_address} • {asset.mac_address || 'No MAC'}</p>
          </div>
        </div>
        <StatusBadge status={asset.is_active ? 'online' : 'offline'} className="text-sm px-3 py-1" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-900/60 border border-slate-800/60 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
              <Network className="w-4 h-4" /> Open Ports & Services
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-800/50">
                    <th className="text-left py-2 px-3 text-xs font-medium text-slate-500 uppercase">Port</th>
                    <th className="text-left py-2 px-3 text-xs font-medium text-slate-500 uppercase">Protocol</th>
                    <th className="text-left py-2 px-3 text-xs font-medium text-slate-500 uppercase">Service</th>
                    <th className="text-left py-2 px-3 text-xs font-medium text-slate-500 uppercase">Version</th>
                  </tr>
                </thead>
                <tbody>
                  {asset.ports?.map((port: any, i: number) => (
                    <tr key={i} className="border-b border-slate-800/30">
                      <td className="py-2.5 px-3 font-mono text-cyan-400 text-xs">{port.port_number}</td>
                      <td className="py-2.5 px-3 text-slate-400 text-xs uppercase">{port.protocol}</td>
                      <td className="py-2.5 px-3 text-slate-200">{port.service?.name || 'Unknown'}</td>
                      <td className="py-2.5 px-3 text-slate-500 text-xs">{port.service?.version || '—'}</td>
                    </tr>
                  ))}
                  {(!asset.ports || asset.ports.length === 0) && (
                    <tr><td colSpan={4} className="py-6 text-center text-slate-600 text-xs">No open ports detected</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800/60 rounded-xl p-5 opacity-50">
            <h2 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
              <Fingerprint className="w-4 h-4" /> Vulnerabilities (Phase 4)
            </h2>
            <p className="text-xs text-slate-500">Vulnerability assessment will be implemented in the next phase.</p>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800/60 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
              <HardDrive className="w-4 h-4" /> Asset Details
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between border-b border-slate-800/50 pb-2">
                <span className="text-xs text-slate-500">Operating System</span>
                <span className="text-sm text-slate-200">{asset.os || 'Unknown'}</span>
              </div>
              <div className="flex justify-between border-b border-slate-800/50 pb-2">
                <span className="text-xs text-slate-500">Vendor</span>
                <span className="text-sm text-slate-200">{asset.vendor || 'Unknown'}</span>
              </div>
              <div className="flex justify-between pb-1">
                <span className="text-xs text-slate-500">Network ID</span>
                <span className="text-sm text-slate-400 font-mono">{asset.network_id || '—'}</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800/60 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
              <Clock className="w-4 h-4" /> Timeline
            </h2>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-cyan-500 mt-1.5" />
                <div>
                  <p className="text-xs text-slate-300">Last Seen</p>
                  <p className="text-[11px] text-slate-500">{formatRelativeTime(asset.last_seen)} ({formatDate(asset.last_seen)})</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-slate-600 mt-1.5" />
                <div>
                  <p className="text-xs text-slate-300">First Discovered</p>
                  <p className="text-[11px] text-slate-500">{formatDate(asset.first_seen)}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
