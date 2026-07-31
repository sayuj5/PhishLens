import React from 'react'
import { cn, statusBg } from '@/utils'

interface StatusBadgeProps {
  status: string
  className?: string
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  return (
    <span className={cn(
      'inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border',
      statusBg(status),
      className
    )}>
      <span className="w-1.5 h-1.5 rounded-full bg-current opacity-80" />
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  )
}
