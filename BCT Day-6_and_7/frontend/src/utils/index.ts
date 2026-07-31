import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | null | undefined): string {
  if (!date) return '—'
  return new Date(date).toLocaleString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

export function formatRelativeTime(date: string | null | undefined): string {
  if (!date) return '—'
  const diff = Date.now() - new Date(date).getTime()
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  return `${Math.floor(hours / 24)}d ago`
}

export function statusColor(status: string): string {
  const map: Record<string, string> = {
    running: 'text-cyan-400',
    completed: 'text-emerald-400',
    failed: 'text-red-400',
    cancelled: 'text-slate-400',
    paused: 'text-amber-400',
    pending: 'text-violet-400',
    online: 'text-emerald-400',
    offline: 'text-red-400',
  }
  return map[status] ?? 'text-slate-400'
}

export function statusBg(status: string): string {
  const map: Record<string, string> = {
    running: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    completed: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    failed: 'bg-red-500/15 text-red-300 border-red-500/30',
    cancelled: 'bg-slate-500/15 text-slate-300 border-slate-500/30',
    paused: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    pending: 'bg-violet-500/15 text-violet-300 border-violet-500/30',
    online: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    offline: 'bg-red-500/15 text-red-300 border-red-500/30',
  }
  return map[status] ?? 'bg-slate-500/15 text-slate-300 border-slate-500/30'
}
