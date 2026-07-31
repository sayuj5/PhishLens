import React, { useState, useEffect, useCallback } from 'react'
import {
  fetchDashboardStats, fetchDiscoveryStats, fetchDiscoveryProgress,
  fetchWorkerStatus, fetchDiscoveryJobs
} from '@/api'
import { KpiCard } from '@/components/ui/KpiCard'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { ProgressBar } from '@/components/ui/ProgressBar'
import { useDiscoverySocket, WsMessage } from '@/hooks/useDiscoverySocket'
import { formatRelativeTime } from '@/utils'
import {
  Server, Wifi, WifiOff, Radar, CheckCircle2, XCircle, Network,
  Activity, AlertTriangle, TrendingUp
} from 'lucide-react'
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  PieChart, Pie, Cell, Legend, BarChart, Bar
} from 'recharts'

const assetGrowthData = [
  { date: 'Mon', assets: 12 }, { date: 'Tue', assets: 19 },
  { date: 'Wed', assets: 24 }, { date: 'Thu', assets: 31 },
  { date: 'Fri', assets: 38 }, { date: 'Sat', assets: 42 },
  { date: 'Sun', assets: 47 },
]
const osData = [
  { name: 'Ubuntu', value: 38, color: '#f97316' },
  { name: 'Windows', value: 29, color: '#3b82f6' },
  { name: 'CentOS', value: 15, color: '#a855f7' },
  { name: 'Other', value: 18, color: '#64748b' },
]
const serviceData = [
  { name: 'SSH', count: 34 }, { name: 'HTTP', count: 29 },
  { name: 'HTTPS', count: 27 }, { name: 'SMB', count: 12 }, { name: 'RDP', count: 8 },
]
const TOOLTIP_STYLE = {
  backgroundColor: '#0f172a', border: '1px solid #1e293b',
  borderRadius: '8px', color: '#e2e8f0', fontSize: '12px',
}

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null)
  const [discStats, setDiscStats] = useState<any>(null)
  const [progress, setProgress] = useState<any[]>([])
  const [workers, setWorkers] = useState<any>(null)
  const [recentJobs, setRecentJobs] = useState<any[]>([])
  const [liveEvents, setLiveEvents] = useState<WsMessage[]>([])
  const [loading, setLoading] = useState(true)

  const loadAll = useCallback(async () => {
    try {
      const [s, ds, p, w, rj] = await Promise.all([
        fetchDashboardStats(),
        fetchDiscoveryStats(),
        fetchDiscoveryProgress(),
        fetchWorkerStatus(),
        fetchDiscoveryJobs(0, 6),
      ])
      setStats(s); setDiscStats(ds)
      setProgress(Array.isArray(p) ? p : [])
      setWorkers(w)
      setRecentJobs(Array.isArray(rj) ? rj : [])
    } catch { /* ignore */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => {
    loadAll()
    const interval = setInterval(loadAll, 30000)
    return () => clearInterval(interval)
  }, [loadAll])

  const handleWsMessage = useCallback((msg: WsMessage) => {
    setLiveEvents(prev => [msg, ...prev].slice(0, 20))
    loadAll()
  }, [loadAll])

  const { connected } = useDiscoverySocket(handleWsMessage)

  return (
    <div className="p-6 space-y-6 min-h-full">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Operations Dashboard</h1>
          <p className="text-sm text-slate-500 mt-0.5">Enterprise asset discovery & inventory</p>
        </div>
        <div className="flex items-center gap-2 text-xs px-3 py-1.5 rounded-full border bg-slate-900/60 border-slate-700/50 text-slate-400">
          <span className={connected ? 'text-emerald-400' : 'text-slate-500'}>?</span>
          {connected ? 'Live updates active' : 'Reconnecting…'}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-4">
        <KpiCard title="Total Assets"   value={stats?.total_assets ?? '—'}       icon={<Server className="w-5 h-5" />}        accent="cyan"    loading={loading} />
        <KpiCard title="Online"         value={stats?.online_hosts ?? '—'}        icon={<Wifi className="w-5 h-5" />}          accent="emerald" loading={loading} />
        <KpiCard title="Offline"        value={stats?.offline_hosts ?? '—'}       icon={<WifiOff className="w-5 h-5" />}       accent="red"     loading={loading} />
        <KpiCard title="Networks"       value={stats?.total_networks ?? '—'}      icon={<Network className="w-5 h-5" />}       accent="violet"  loading={loading} />
        <KpiCard title="Avg Risk Score" value={stats ? (stats.average_risk_score as number).toFixed(1) : '—'} icon={<AlertTriangle className="w-5 h-5" />} accent="amber" loading={loading} />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KpiCard title="Running Jobs"   value={discStats?.running_jobs ?? '—'}   icon={<Radar className="w-5 h-5" />}         accent="cyan"    loading={!discStats} />
        <KpiCard title="Completed Jobs" value={discStats?.completed_jobs ?? '—'} icon={<CheckCircle2 className="w-5 h-5" />} accent="emerald" loading={!discStats} />
        <KpiCard title="Failed Jobs"    value={discStats?.failed_jobs ?? '—'}    icon={<XCircle className="w-5 h-5" />}      accent="red"     loading={!discStats} />
        <KpiCard title="Total Scanned"  value={discStats?.total_results ?? '—'}  icon={<TrendingUp className="w-5 h-5" />}   accent="violet"  loading={!discStats} />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 rounded-xl border border-slate-800/60 bg-slate-900/60 p-5">
          <h3 className="text-sm font-semibold text-slate-300 mb-4">Asset Growth (7d)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={assetGrowthData}>
              <defs>
                <linearGradient id="assetGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={TOOLTIP_STYLE} />
              <Area type="monotone" dataKey="assets" stroke="#06b6d4" strokeWidth={2} fill="url(#assetGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 p-5">
          <h3 className="text-sm font-semibold text-slate-300 mb-4">OS Distribution</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={osData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={3} dataKey="value">
                {osData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
              </Pie>
              <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }} />
              <Tooltip contentStyle={TOOLTIP_STYLE} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 p-5">
          <h3 className="text-sm font-semibold text-slate-300 mb-4">Top Services</h3>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={serviceData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
              <XAxis type="number" tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} tickLine={false} />
              <YAxis dataKey="name" type="category" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} width={40} />
              <Tooltip contentStyle={TOOLTIP_STYLE} />
              <Bar dataKey="count" fill="#06b6d4" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-300">Worker Pool</h3>
            <span className="text-xs text-slate-500">{workers?.num_workers ?? '—'} workers</span>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between text-xs text-slate-400">
              <span>Queue Length</span>
              <span className="text-slate-200 font-mono">{workers?.queue_size ?? 0}</span>
            </div>
            <div className="flex justify-between text-xs text-slate-400">
              <span>Active Jobs</span>
              <span className="text-slate-200 font-mono">{workers?.active_jobs?.length ?? 0}</span>
            </div>
            {progress.map((p: any) => (
              <div key={p.job_id} className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Job #{p.job_id}</span>
                  <span className="text-cyan-400">{p.tasks_remaining} remaining</span>
                </div>
                <ProgressBar value={0} color="cyan" size="sm" />
              </div>
            ))}
            {progress.length === 0 && <p className="text-xs text-slate-600 text-center py-2">No active jobs</p>}
          </div>
        </div>

        <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-300">Live Events</h3>
            <Activity className="w-4 h-4 text-slate-600" />
          </div>
          <div className="space-y-2 max-h-44 overflow-y-auto">
            {liveEvents.length === 0 && <p className="text-xs text-slate-600 text-center py-4">Listening for events…</p>}
            {liveEvents.map((evt, i) => (
              <div key={i} className="flex items-start gap-2 text-xs border-b border-slate-800/50 pb-2">
                <span className="text-cyan-500 mt-0.5">?</span>
                <div>
                  <span className="text-slate-300">{evt.status ?? 'event'}</span>
                  {evt.target && <span className="text-slate-500"> – {evt.target as string}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-800/60">
          <h3 className="text-sm font-semibold text-slate-300">Recent Discovery Jobs</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-800/50">
                {['ID', 'Target', 'Type', 'Status', 'Created', 'Duration'].map(h => (
                  <th key={h} className="text-left px-5 py-3 text-xs font-medium text-slate-500 uppercase tracking-wider">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading && [...Array(4)].map((_, i) => (
                <tr key={i} className="border-b border-slate-800/30">
                  {[...Array(6)].map((_, j) => (
                    <td key={j} className="px-5 py-3"><div className="h-4 bg-slate-800 rounded animate-pulse" /></td>
                  ))}
                </tr>
              ))}
              {recentJobs.map((j: any) => {
                const duration = j.start_time && j.end_time
                  ? `${Math.round((new Date(j.end_time).getTime() - new Date(j.start_time).getTime()) / 1000)}s` : '—'
                return (
                  <tr key={j.id} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                    <td className="px-5 py-3 font-mono text-xs text-slate-400">#{j.id}</td>
                    <td className="px-5 py-3 text-slate-200 font-mono text-xs">{j.target}</td>
                    <td className="px-5 py-3 text-slate-400 capitalize">{j.job_type}</td>
                    <td className="px-5 py-3"><StatusBadge status={j.status} /></td>
                    <td className="px-5 py-3 text-slate-500 text-xs">{formatRelativeTime(j.created_at)}</td>
                    <td className="px-5 py-3 text-slate-500 text-xs font-mono">{duration}</td>
                  </tr>
                )
              })}
              {!loading && recentJobs.length === 0 && (
                <tr><td colSpan={6} className="px-5 py-10 text-center text-slate-600 text-sm">No discovery jobs yet. Start one from the Discovery page.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
