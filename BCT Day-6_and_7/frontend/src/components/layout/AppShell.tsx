import React, { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { cn } from '@/utils'
import { Bell, Wifi, WifiOff } from 'lucide-react'
import { useDiscoverySocket } from '@/hooks/useDiscoverySocket'

export function AppShell() {
  const [collapsed, setCollapsed] = useState(false)
  const { connected } = useDiscoverySocket(() => {})

  return (
    <div className="flex h-screen bg-[#080c14] text-slate-100 overflow-hidden">
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} />
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="shrink-0 flex items-center justify-between px-6 h-14 border-b border-slate-800/60 bg-slate-950/70 backdrop-blur-sm">
          <div />
          <div className="flex items-center gap-3">
            <div className={cn(
              'flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full border',
              connected
                ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10'
                : 'text-slate-500 border-slate-700/50 bg-slate-800/50'
            )}>
              {connected ? <Wifi className="w-3 h-3" /> : <WifiOff className="w-3 h-3" />}
              {connected ? 'Live' : 'Offline'}
            </div>
            <button className="relative p-1.5 rounded-lg hover:bg-slate-800 transition-colors text-slate-400 hover:text-slate-200">
              <Bell className="w-4 h-4" />
            </button>
          </div>
        </header>
        {/* Page Content */}
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
