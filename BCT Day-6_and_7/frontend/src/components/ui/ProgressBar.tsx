import React from 'react'
import { cn } from '@/utils'

interface ProgressBarProps {
  value: number
  className?: string
  size?: 'sm' | 'md'
  color?: 'cyan' | 'emerald' | 'amber' | 'red'
  showLabel?: boolean
}

const colorMap = {
  cyan:    'bg-gradient-to-r from-cyan-600 to-cyan-400',
  emerald: 'bg-gradient-to-r from-emerald-600 to-emerald-400',
  amber:   'bg-gradient-to-r from-amber-600 to-amber-400',
  red:     'bg-gradient-to-r from-red-600 to-red-400',
}

export function ProgressBar({ value, className, size = 'md', color = 'cyan', showLabel }: ProgressBarProps) {
  const clamped = Math.min(100, Math.max(0, value))
  const h = size === 'sm' ? 'h-1' : 'h-2'
  return (
    <div className={cn('flex items-center gap-3', className)}>
      <div className={cn('flex-1 bg-slate-800 rounded-full overflow-hidden', h)}>
        <div
          className={cn('h-full rounded-full transition-all duration-500', colorMap[color])}
          style={{ width: `${clamped}%` }}
        />
      </div>
      {showLabel && <span className="text-xs text-slate-400 tabular-nums w-10 text-right">{clamped.toFixed(0)}%</span>}
    </div>
  )
}
