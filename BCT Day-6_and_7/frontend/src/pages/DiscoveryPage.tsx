import React, { useState, useEffect } from 'react'
import {
  fetchDiscoveryJobs, startDiscoveryJob, pauseJob, resumeJob, cancelJob
} from '@/api'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { formatRelativeTime } from '@/utils'
import { Radar, Play, Pause, XCircle, Settings2, Shield } from 'lucide-react'

export default function DiscoveryPage() {
  const [jobs, setJobs] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [target, setTarget] = useState('')
  const [jobType, setJobType] = useState('ping')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [error, setError] = useState('')

  const loadJobs = async () => {
    try {
      const data = await fetchDiscoveryJobs(0, 50)
      setJobs(Array.isArray(data) ? data : [])
    } catch { /* ignore */ }
    finally { setLoading(false) }
  }

  useEffect(() => {
    loadJobs()
    const interval = setInterval(loadJobs, 15000)
    return () => clearInterval(interval)
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!target) return
    setIsSubmitting(true)
    setError('')
    try {
      await startDiscoveryJob(target, jobType)
      setShowModal(false)
      setTarget('')
      loadJobs()
    } catch (err: any) {
      setError(err.message || 'Failed to start job')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleAction = async (id: number, action: 'pause' | 'resume' | 'cancel') => {
    try {
      if (action === 'pause') await pauseJob(id)
      if (action === 'resume') await resumeJob(id)
      if (action === 'cancel') await cancelJob(id)
      loadJobs()
    } catch { /* ignore */ }
  }

  return (
    <div className="p-6 space-y-6 min-h-full relative">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <Radar className="w-6 h-6 text-cyan-400" /> Discovery Jobs
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">Manage network scans and asset discovery tasks</p>
        </div>
        <button onClick={() => setShowModal(true)} className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-medium transition-colors shadow-lg shadow-cyan-500/20">
          <Play className="w-4 h-4" /> New Discovery Scan
        </button>
      </div>

      <div className="rounded-xl border border-slate-800/60 bg-slate-900/60 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-800/60 bg-slate-950/50">
                {['ID', 'Target', 'Type', 'Status', 'Tasks', 'Created', 'Actions'].map(h => (
                  <th key={h} className="text-left px-5 py-3.5 text-xs font-medium text-slate-500 uppercase tracking-wider whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading && [...Array(5)].map((_, i) => (
                <tr key={i} className="border-b border-slate-800/30">
                  {[...Array(7)].map((_, j) => (
                    <td key={j} className="px-5 py-3.5"><div className="h-4 bg-slate-800 rounded animate-pulse w-24" /></td>
                  ))}
                </tr>
              ))}
              {jobs.map((job: any) => (
                <tr key={job.id} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                  <td className="px-5 py-3.5 font-mono text-xs text-slate-500">#{job.id}</td>
                  <td className="px-5 py-3.5 text-slate-200 font-mono text-xs">{job.target}</td>
                  <td className="px-5 py-3.5 text-slate-400 text-xs capitalize">{job.job_type}</td>
                  <td className="px-5 py-3.5"><StatusBadge status={job.status} /></td>
                  <td className="px-5 py-3.5 text-slate-400 text-xs font-mono">{job.tasks_total || '—'}</td>
                  <td className="px-5 py-3.5 text-slate-500 text-xs whitespace-nowrap">{formatRelativeTime(job.created_at)}</td>
                  <td className="px-5 py-3.5">
                    <div className="flex items-center gap-1.5">
                      {job.status === 'running' && (
                        <button onClick={() => handleAction(job.id, 'pause')} className="p-1.5 text-amber-400 hover:bg-amber-400/10 rounded" title="Pause">
                          <Pause className="w-4 h-4" />
                        </button>
                      )}
                      {job.status === 'paused' && (
                        <button onClick={() => handleAction(job.id, 'resume')} className="p-1.5 text-emerald-400 hover:bg-emerald-400/10 rounded" title="Resume">
                          <Play className="w-4 h-4" />
                        </button>
                      )}
                      {['running', 'pending', 'paused'].includes(job.status) && (
                        <button onClick={() => handleAction(job.id, 'cancel')} className="p-1.5 text-red-400 hover:bg-red-400/10 rounded" title="Cancel">
                          <XCircle className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
              {!loading && jobs.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-5 py-16 text-center">
                    <Radar className="w-10 h-10 text-slate-700 mx-auto mb-3" />
                    <p className="text-slate-500 text-sm">No discovery jobs found</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="absolute inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="w-full max-w-md bg-slate-900 border border-slate-700/60 rounded-xl shadow-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">New Discovery Scan</h2>
            {error && <div className="mb-4 p-3 text-xs text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg">{error}</div>}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1.5">Target (IP, CIDR, or Hostname)</label>
                <input
                  value={target} onChange={e => setTarget(e.target.value)}
                  placeholder="e.g. 192.168.1.0/24 or 10.0.0.1"
                  className="w-full px-3 py-2 bg-slate-800/70 border border-slate-700/60 rounded-lg text-sm text-white focus:outline-none focus:border-cyan-500/50"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1.5">Scan Type</label>
                <select
                  value={jobType} onChange={e => setJobType(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-800/70 border border-slate-700/60 rounded-lg text-sm text-white focus:outline-none focus:border-cyan-500/50"
                >
                  <option value="ping">Ping Sweep (Fast)</option>
                  <option value="arp">ARP Discovery (Local only)</option>
                  <option value="syn">SYN Port Scan (Stealth)</option>
                  <option value="full">Full Port Scan (1-65535)</option>
                </select>
              </div>
              <div className="bg-cyan-500/10 border border-cyan-500/20 p-3 rounded-lg flex items-start gap-3 mt-2">
                <Shield className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                <p className="text-[11px] text-cyan-200/70">Only scan networks you are authorised to test. All activities are logged.</p>
              </div>
              <div className="flex justify-end gap-3 pt-4 border-t border-slate-800/60 mt-6">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 text-sm font-medium text-slate-400 hover:text-white transition-colors">Cancel</button>
                <button type="submit" disabled={isSubmitting || !target} className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50">
                  {isSubmitting ? 'Starting…' : 'Launch Scan'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
