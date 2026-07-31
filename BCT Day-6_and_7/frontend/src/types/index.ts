// Shared TypeScript types for BlackFalcon

export interface Asset {
  id: number
  ip_address: string
  hostname?: string
  mac_address?: string
  os?: string
  vendor?: string
  is_active: boolean
  network_id?: number
  first_seen?: string
  last_seen?: string
  ports?: Port[]
}

export interface Port {
  port_number: number
  protocol: string
  service: { name: string; version: string } | null
}

export interface DiscoveryJob {
  id: number
  target: string
  job_type: string
  status: string
  created_at: string
  start_time?: string
  end_time?: string
}

export interface AssessmentJob {
  id: number
  asset_id: number
  status: string
  start_time?: string
  findings_count?: number
  critical_count?: number
  high_count?: number
  medium_count?: number
}

export interface Finding {
  id: number
  title: string
  description: string
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  status: 'open' | 'acknowledged' | 'resolved' | 'false_positive'
  asset_id: number
  category: string
  plugin_ref: string
  first_seen: string
  last_seen: string
  evidence?: string
  remediation?: string
}

export interface DashboardStats {
  total_assets: number
  online_hosts: number
  offline_hosts: number
  total_networks: number
  average_risk_score: number
}

export interface DiscoveryStats {
  total_jobs: number
  running_jobs: number
  completed_jobs: number
  failed_jobs: number
  total_results: number
}

export interface WorkerStatus {
  num_workers: number
  queue_size: number
  active_jobs: number[]
}

export interface ProgressEntry {
  job_id: number
  tasks_remaining: number
  status: string
}

export interface RiskSummary {
  asset_id: number
  ip_address?: string
  hostname?: string
  risk_score: number
  critical: number
  high: number
  medium: number
  low: number
}

export interface AssessmentStats {
  open_findings: number
  critical_findings: number
  high_findings: number
}

export interface Profile {
  id: number
  name: string
}
