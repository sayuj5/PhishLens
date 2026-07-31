import React, { useState, useEffect } from 'react'
import { fetchAssets } from '@/api'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { formatRelativeTime, formatDate } from '@/utils'
import { Search, Download, Filter, Server, ChevronLeft, ChevronRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const PAGE_SIZE = 20

export default function AssetsPage() {
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(0)
  const [assets, setAssets] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        const data = await fetchAssets(page * PAGE_SIZE, PAGE_SIZE)
        if (active) setAssets(Array.isArray(data) ? data : [])
      } catch { /* ignore */ }
      finally { if (active) setIsLoading(false) }
    }
    load()
    const interval = setInterval(load, 30000)
    return () => { active = false; clearInterval(interval) }
  }, [page])

  const filtered = assets.filter((a: any) => {
    const q = search.toLowerCase()
    return (
      a.hostname?.toLowerCase().includes(q) ||
      a.ip_address?.toLowerCase().includes(q) ||
      a.os?.toLowerCase().includes(q) ||
      a.vendor?.toLowerCase().includes(q)
    )
  })

  function exportCsv() {
    const rows = [['ID', 'IP', 'Hostname', 'OS', 'Vendor', 'Status', 'First Seen', 'Last Seen']]
    filtered.forEach((a: any) => {
      rows.push([
        String(a.id ?? ''), a.ip_address ?? '', a.hostname ?? '',
        a.os ?? '', a.vendor ?? '',
        a.is_active ? 'online' : 'offline',
        formatDate(a.first_seen), formatDate(a.last_seen),
      ])
    })
    const csv = rows.map(r => r.join(',')).join('\n')
    const link = document.createElement('a')
    link.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }))
    link.download = 'blackfalcon-assets.csv'
    link.click()
  }

  return (
    <div className="p-6 space-y-5 min-h-full">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <Server className="w-6 h-6 text-cyan-400" />
            Asset Inventory
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">
            {!isLoading ? `${assets.length} assets discovered` : 'Loading…'}
          </p>
        </div>
        <button onClick={exportCsv} className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm border border-slate-700/60 transition-colors">
          <Download className="w-4 h-4" /> Export CSV
        </button>
      </div>

      <div className="flex gap-3">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search by IP, hostname, OS…"
            className="w-full pl-9 pr-4 py-2 bg-slate-900/70 border border-slate-700/60 rounded-lg text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-cyan-500/50 transition-colors"
          />
        </div>
        <button className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-900/70 border border-slate-700/60 text-slate-400 hover:text-slate-200 text-sm transition-colors">
          <Filter className="w-4 h-4" /> Filter
        </button>
      </div>

      <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-800/60 bg-slate-950/50">
                {['#', 'IP Address', 'Hostname', 'OS', 'Vendor', 'Status', 'Open Ports', 'Last Seen', 'First Seen'].map(h => (
                  <th key={h} className="text-left px-5 py-3.5 text-xs font-medium text-slate-500 uppercase tracking-wider whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {isLoading && [...Array(8)].map((_, i) => (
                <tr key={i} className="border-b border-slate-800/30">
                  {[...Array(9)].map((_, j) => (
                    <td key={j} className="px-5 py-3.5">
                      <div className="h-4 bg-slate-800 rounded animate-pulse" style={{ width: `${60 + Math.random() * 40}%` }} />
                    </td>
                  ))}
                </tr>
              ))}
              {filtered.map((asset: any) => (
                <tr key={asset.id} onClick={() => navigate(`/assets/${asset.id}`)} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors cursor-pointer group">
                  <td className="px-5 py-3.5 font-mono text-xs text-slate-500">#{asset.id}</td>
                  <td className="px-5 py-3.5 font-mono text-xs text-cyan-400">{asset.ip_address ?? '—'}</td>
                  <td className="px-5 py-3.5 text-slate-200 font-medium">{asset.hostname ?? '—'}</td>
                  <td className="px-5 py-3.5 text-slate-400 text-xs">{asset.os ?? '—'}</td>
                  <td className="px-5 py-3.5 text-slate-400 text-xs">{asset.vendor ?? '—'}</td>
                  <td className="px-5 py-3.5"><StatusBadge status={asset.is_active ? 'online' : 'offline'} /></td>
                  <td className="px-5 py-3.5 text-slate-400 text-xs font-mono">{asset.ports?.length ?? 0}</td>
                  <td className="px-5 py-3.5 text-slate-500 text-xs whitespace-nowrap">{formatRelativeTime(asset.last_seen)}</td>
                  <td className="px-5 py-3.5 text-slate-600 text-xs whitespace-nowrap">{formatRelativeTime(asset.first_seen)}</td>
                </tr>
              ))}
              {!isLoading && filtered.length === 0 && (
                <tr>
                  <td colSpan={9} className="px-5 py-16 text-center">
                    <Server className="w-10 h-10 text-slate-700 mx-auto mb-3" />
                    <p className="text-slate-500 text-sm">No assets found</p>
                    <p className="text-slate-700 text-xs mt-1">Run a discovery scan to populate your inventory</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="flex items-center justify-between px-5 py-3 border-t border-slate-800/60 bg-slate-950/30">
          <span className="text-xs text-slate-500">Showing {page * PAGE_SIZE + (filtered.length ? 1 : 0)}–{page * PAGE_SIZE + filtered.length}</span>
          <div className="flex items-center gap-2">
            <button disabled={page === 0} onClick={() => setPage(p => p - 1)} className="p-1.5 rounded hover:bg-slate-800 disabled:opacity-30 transition-colors text-slate-400">
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs text-slate-400">Page {page + 1}</span>
            <button disabled={filtered.length < PAGE_SIZE} onClick={() => setPage(p => p + 1)} className="p-1.5 rounded hover:bg-slate-800 disabled:opacity-30 transition-colors text-slate-400">
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
