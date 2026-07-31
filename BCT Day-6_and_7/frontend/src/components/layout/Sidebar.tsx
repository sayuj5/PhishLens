import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { cn } from '@/utils'
import {
  LayoutDashboard, Server, Network, Radar, Briefcase,
  Activity, Settings, ChevronLeft, ChevronRight,
  FileBarChart, Shield, HeartPulse, LogOut, Search,
  Target, ShieldAlert, TrendingUp
} from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

const navItems = [
  { href: '/dashboard',        label: 'Dashboard',    icon: LayoutDashboard },
  { href: '/risk',             label: 'Risk',          icon: TrendingUp      },
  { href: '/assets',           label: 'Assets',        icon: Server          },
  { href: '/networks',         label: 'Networks',      icon: Network         },
  { href: '/vulnerabilities',  label: 'Findings',      icon: ShieldAlert     },
  { href: '/assessment',       label: 'Assessment',    icon: Target          },
  { href: '/discovery',        label: 'Discovery',     icon: Radar           },
  { href: '/jobs',             label: 'Jobs',          icon: Briefcase       },
  { href: '/activity',         label: 'Activity',      icon: Activity        },
  { href: '/health',           label: 'System Health', icon: HeartPulse      },
]

const disabledItems = [
  { label: 'Reports',    icon: FileBarChart },
  { label: 'Compliance', icon: Shield },
]

const bottomItems = [
  { href: '/settings', label: 'Settings', icon: Settings },
]

interface SidebarProps {
  collapsed: boolean
  onToggle: () => void
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <aside className={cn(
      'flex flex-col h-full bg-slate-950/95 border-r border-slate-800/60 transition-all duration-300',
      collapsed ? 'w-16' : 'w-60'
    )}>
      {/* Brand */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-slate-800/60">
        <div className="shrink-0 w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/25">
          <Shield className="w-4 h-4 text-white" strokeWidth={2.5} />
        </div>
        {!collapsed && (
          <div>
            <p className="text-sm font-bold text-white tracking-tight">BlackFalcon</p>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest">Enterprise</p>
          </div>
        )}
      </div>

      {/* Search */}
      {!collapsed && (
        <div className="px-3 py-3">
          <NavLink to="/search" className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-900/80 border border-slate-800/60 text-slate-400 text-sm hover:border-slate-700 transition-colors">
            <Search className="w-3.5 h-3.5" />
            <span className="flex-1 text-xs">Search…</span>
            <kbd className="text-[10px] bg-slate-800 px-1 rounded">?K</kbd>
          </NavLink>
        </div>
      )}

      {/* Nav */}
      <nav className="flex-1 px-2 py-2 space-y-0.5 overflow-y-auto">
        {navItems.map(({ href, label, icon: Icon }) => (
          <NavLink
            key={href}
            to={href}
            className={({ isActive }) => cn(
              'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group relative',
              isActive
                ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'
                : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 border border-transparent'
            )}
          >
            {({ isActive }) => (
              <>
                <Icon className={cn('w-4 h-4 shrink-0', isActive ? 'text-cyan-400' : 'group-hover:text-slate-200')} />
                {!collapsed && <span className="truncate">{label}</span>}
                {collapsed && (
                  <div className="absolute left-full ml-3 px-2 py-1 bg-slate-800 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50 shadow-xl">
                    {label}
                  </div>
                )}
              </>
            )}
          </NavLink>
        ))}

        {/* Disabled section */}
        <div className="pt-2">
          {!collapsed && <p className="px-3 pb-1 text-[10px] font-semibold text-slate-600 uppercase tracking-widest">Coming Soon</p>}
          {disabledItems.map(({ label, icon: Icon }) => (
            <div key={label} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm opacity-30 cursor-not-allowed select-none text-slate-500">
              <Icon className="w-4 h-4 shrink-0" />
              {!collapsed && <span className="truncate">{label}</span>}
            </div>
          ))}
        </div>
      </nav>

      {/* Bottom */}
      <div className="px-2 pb-2 space-y-0.5 border-t border-slate-800/60 pt-2">
        {bottomItems.map(({ href, label, icon: Icon }) => (
          <NavLink key={href} to={href} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 transition-all border border-transparent">
            <Icon className="w-4 h-4 shrink-0" />
            {!collapsed && <span className="truncate">{label}</span>}
          </NavLink>
        ))}
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-400 hover:bg-red-500/10 hover:text-red-400 transition-all border border-transparent"
        >
          <LogOut className="w-4 h-4 shrink-0" />
          {!collapsed && <span>Logout</span>}
        </button>
        <button
          onClick={onToggle}
          className="w-full flex items-center justify-center py-2 text-slate-600 hover:text-slate-400 transition-colors"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>
    </aside>
  )
}
