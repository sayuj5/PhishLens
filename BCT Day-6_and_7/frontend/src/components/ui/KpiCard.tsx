import React from 'react'
import { cn } from '@/utils'

interface KpiCardProps {
  title: string
  value: number | string
  icon: React.ReactNode
  trend?: string
  accent?: 'cyan' | 'emerald' | 'red' | 'amber' | 'violet' | 'slate'
  loading?: boolean
}

const accentMap = {
  cyan:    'border-cyan-500/30 shadow-cyan-500/5',
  emerald: 'border-emerald-500/30 shadow-emerald-500/5',
  red:     'border-red-500/30 shadow-red-500/5',
  amber:   'border-amber-500/30 shadow-amber-500/5',
  violet:  'border-violet-500/30 shadow-violet-500/5',
  slate:   'border-slate-700/50 shadow-slate-900/10',
}

const iconAccentMap = {
  cyan:    'text-cyan-400 bg-cyan-500/10',
  emerald: 'text-emerald-400 bg-emerald-500/10',
  red:     'text-red-400 bg-red-500/10',
  amber:   'text-amber-400 bg-amber-500/10',
  violet:  'text-violet-400 bg-violet-500/10',
  slate:   'text-slate-400 bg-slate-500/10',
}

export function KpiCard({ title, value, icon, trend, accent = 'slate', loading }: KpiCardProps) {
  return (
    <div className={cn(
      'relative rounded-xl border bg-slate-900/60 backdrop-blur-sm p-5 shadow-lg transition-all duration-200 hover:shadow-xl hover:-translate-y-0.5',
      accentMap[accent]
    )}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-slate-400 uppercase tracking-widest mb-2">{title}</p>
          {loading ? (
            <div className="h-8 w-20 bg-slate-800 rounded animate-pulse" />
          ) : (
            <p className="text-3xl font-bold text-white tabular-nums">{value}</p>
          )}
          {trend && <p className="text-xs text-slate-500 mt-1.5">{trend}</p>}
        </div>
        <div className={cn('p-2.5 rounded-lg', iconAccentMap[accent])}>
          {icon}
        </div>
      </div>
      <div className={cn('absolute top-0 left-4 right-4 h-px opacity-40',
        accent === 'cyan' ? 'bg-cyan-500' :
        accent === 'emerald' ? 'bg-emerald-500' :
        accent === 'red' ? 'bg-red-500' :
        accent === 'amber' ? 'bg-amber-500' :
        accent === 'violet' ? 'bg-violet-500' : 'bg-slate-600'
      )} />
    </div>
  )
}
