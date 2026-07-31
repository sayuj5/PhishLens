import React from 'react'
import { Activity } from 'lucide-react'

export default function ActivityPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white flex items-center gap-2.5 mb-2">
        <Activity className="w-6 h-6 text-slate-400" /> Audit Log
      </h1>
      <p className="text-slate-500">Activity and audit logging will be implemented in a future update.</p>
    </div>
  )
}
