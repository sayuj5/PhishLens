/**
 * BlackFalcon API Client
 * Uses native fetch() - no axios dependency
 * VITE_API_URL env variable (default: http://localhost:8000 via proxy)
 */

function getToken(): string | null {
  return localStorage.getItem('bf_token')
}

function authHeaders(): Record<string, string> {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...(options.headers as Record<string, string> ?? {}),
    },
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status}: ${text}`)
  }
  const text = await res.text()
  return text ? JSON.parse(text) : ({} as T)
}

function qs(params?: Record<string, unknown>): string {
  if (!params) return ''
  const q = new URLSearchParams(
    Object.entries(params)
      .filter(([, v]) => v !== undefined && v !== null && v !== '')
      .map(([k, v]) => [k, String(v)])
  )
  const s = q.toString()
  return s ? `?${s}` : ''
}

// --- Auth ---------------------------------------------------------------------
export async function login(email: string, password: string) {
  const form = new URLSearchParams({ username: email, password })
  const res = await fetch('/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form.toString(),
  })
  if (!res.ok) throw new Error('Login failed')
  return res.json() as Promise<{ access_token: string; token_type: string }>
}

// --- Dashboard ----------------------------------------------------------------
export async function fetchDashboardStats() {
  return request<any>('/api/dashboard/')
}

// --- Assets -------------------------------------------------------------------
export async function fetchAssets(skip = 0, limit = 100) {
  return request<any[]>(`/api/assets/${qs({ skip, limit })}`)
}

export async function fetchAsset(id: number) {
  return request<any>(`/api/assets/${id}`)
}

// --- Networks -----------------------------------------------------------------
export async function fetchNetworks(skip = 0, limit = 100) {
  return request<any[]>(`/api/networks/${qs({ skip, limit })}`)
}

// --- Discovery ----------------------------------------------------------------
export async function fetchDiscoveryJobs(skip = 0, limit = 50) {
  return request<any[]>(`/api/discovery/jobs${qs({ skip, limit })}`)
}

export async function fetchDiscoveryJob(id: number) {
  return request<any>(`/api/discovery/jobs/${id}`)
}

export async function startDiscoveryJob(target: string, jobType: string, profileId?: number) {
  return request<any>('/api/discovery/start', {
    method: 'POST',
    body: JSON.stringify({ target, job_type: jobType, profile_id: profileId }),
  })
}

export async function cancelJob(id: number) {
  return request<any>(`/api/discovery/cancel/${id}`, { method: 'POST' })
}

export async function pauseJob(id: number) {
  return request<any>(`/api/discovery/pause/${id}`, { method: 'POST' })
}

export async function resumeJob(id: number) {
  return request<any>(`/api/discovery/resume/${id}`, { method: 'POST' })
}

export async function fetchDiscoveryProgress() {
  return request<any[]>('/api/discovery/progress')
}

export async function fetchWorkerStatus() {
  return request<any>('/api/discovery/workers')
}

export async function fetchDiscoveryStats() {
  return request<any>('/api/discovery/statistics')
}

export async function fetchDiscoveryHistory(skip = 0, limit = 100) {
  return request<any[]>(`/api/discovery/history${qs({ skip, limit })}`)
}

export async function fetchProfiles() {
  return request<any[]>('/api/discovery/profiles')
}

export async function fetchScopes() {
  return request<any[]>('/api/discovery/scopes')
}

export async function globalSearch(q: string) {
  return request<any>(`/api/search/${qs({ q })}`)
}

// --- Assessment ---------------------------------------------------------------
export async function fetchAssessmentJobs(skip = 0, limit = 50) {
  return request<any[]>(`/api/assessment/jobs${qs({ skip, limit })}`)
}

export async function startAssessmentJob(assetId: number, policyId?: number) {
  return request<any>('/api/assessment/jobs', {
    method: 'POST',
    body: JSON.stringify({ asset_id: assetId, policy_id: policyId }),
  })
}

export async function fetchFindings(skip = 0, limit = 50, params: Record<string, unknown> = {}) {
  return request<any[]>(`/api/assessment/findings${qs({ skip, limit, ...params })}`)
}

export async function fetchFinding(id: number) {
  return request<any>(`/api/assessment/findings/${id}`)
}

export async function updateFindingStatus(id: number, status: string, note?: string) {
  return request<any>(`/api/assessment/findings/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ status, note }),
  })
}

export async function fetchRiskSummary() {
  return request<any[]>('/api/assessment/risk-summary')
}

export async function fetchAssessmentStats() {
  return request<any>('/api/assessment/statistics')
}
