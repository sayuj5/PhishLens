import React, { useState, useEffect } from 'react'
import { fetchAssessmentJobs, startAssessmentJob, fetchAssets } from '@/api'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { formatRelativeTime } from '@/utils'
import { Target, Play } from 'lucide-react'

export default function AssessmentPage() {
  const [jobs, setJobs] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [assets, setAssets] = useState<any[]>([])
  const [showModal, setShowModal] = useState(false)
  const [selectedAsset, setSelectedAsset] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const loadData = async () => {
    try {
      const [j, a] = await Promise.all([fetchAssessmentJobs(0, 50), fetchAssets(0, 100)])
      setJobs(Array.isArray(j) ? j : [])
      setAssets(Array.isArray(a) ? a : [])
    } catch { /* ignore */ }
    finally { setLoading(false) }
  }

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 15000)
    return () => clearInterval(interval)
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedAsset) return
    setIsSubmitting(true)
    try {
      await startAssessmentJob(Number(selectedAsset))
      setShowModal(false)
      setSelectedAsset('')
      loadData()
    } catch { /* ignore */ }
    finally { setIsSubmitting(false) }
  }

  return (
    <div className="p-6 space-y-6 min-h-full">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <Target className="w-6 h-6 text-cyan-400" /> Vulnerability Assessment
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">Run active scans against discovered assets</p>
        </div>
        <button onClick={() => setShowModal(true)} className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-medium transition-colors shadow-lg shadow-cyan-500/20">
          <Play className="w-4 h-4" /> Start Assessment
        </button>
      </div>

      <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="bg-slate-950/50 border-b border-slate-800/60">
            <tr>
              {['ID', 'Asset IP', 'Status', 'Findings Found', 'Started', 'Duration'].map(h => (
                <th key={h} className="px-5 py-3.5 text-xs font-medium text-slate-500 uppercase">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading && [...Array(3)].map((_, i) => (
              <tr key={i} className="border-b border-slate-800/30"><td colSpan={6} className="px-5 py-3.5"><div className="h-4 bg-slate-800 rounded animate-pulse" /></td></tr>
            ))}
            {jobs.map(job => (
              <tr key={job.id} className="border-b border-slate-800/30 hover:bg-slate-800/20">
                <td className="px-5 py-3.5 font-mono text-xs text-slate-500">#{job.id}</td>
                <td className="px-5 py-3.5 font-mono text-cyan-400 text-xs">{job.asset?.ip_address || '—'}</td>
                <td className="px-5 py-3.5"><StatusBadge status={job.status} /></td>
                <td className="px-5 py-3.5 text-slate-400 text-xs">
                  {job.status === 'completed' ? (
                    <span className="flex gap-2">
                      <span className="text-red-400">{job.critical_count}C</span>
                      <span className="text-amber-400">{job.high_count}H</span>
                      <span className="text-yellow-400">{job.medium_count}M</span>
                    </span>
                  ) : '—'}
                </td>
                <td className="px-5 py-3.5 text-slate-500 text-xs">{formatRelativeTime(job.start_time)}</td>
                <td className="px-5 py-3.5 text-slate-500 text-xs">
                  {job.start_time && job.end_time ? `${Math.round((new Date(job.end_time).getTime() - new Date(job.start_time).getTime()) / 1000)}s` : '—'}
                </td>
              </tr>
            ))}
            {!loading && jobs.length === 0 && (
              <tr><td colSpan={6} className="px-5 py-10 text-center text-slate-500">No assessments run yet.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="absolute inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="w-full max-w-md bg-slate-900 border border-slate-700/60 rounded-xl shadow-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">Start Assessment</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1.5">Select Asset</label>
                <select value={selectedAsset} onChange={e => setSelectedAsset(e.target.value)} required className="w-full px-3 py-2 bg-slate-800/70 border border-slate-700/60 rounded-lg text-sm text-white focus:outline-none focus:border-cyan-500/50">
                  <option value="" disabled>Choose an asset…</option>
                  {assets.filter(a => a.is_active).map(a => (
                    <option key={a.id} value={a.id}>{a.ip_address} {a.hostname ? `(${a.hostname})` : ''}</option>
                  ))}
                </select>
              </div>
              <div className="flex justify-end gap-3 pt-4 mt-6 border-t border-slate-800/60">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 text-sm text-slate-400 hover:text-white">Cancel</button>
                <button type="submit" disabled={isSubmitting || !selectedAsset} className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-sm rounded-lg disabled:opacity-50">Launch</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
