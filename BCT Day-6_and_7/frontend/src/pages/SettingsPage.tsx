import React from 'react'
import { Settings } from 'lucide-react'

export default function SettingsPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white flex items-center gap-2.5 mb-2">
        <Settings className="w-6 h-6 text-slate-400" /> Settings
      </h1>
      <p className="text-slate-500">Global platform settings and user management.</p>
    </div>
  )
}
