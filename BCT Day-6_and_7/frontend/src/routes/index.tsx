import React, { lazy } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AppShell } from '@/components/layout/AppShell'
import { useAuth } from '@/contexts/AuthContext'

// Lazy-loaded pages
const LoginPage           = lazy(() => import('@/pages/LoginPage'))
const DashboardPage       = lazy(() => import('@/pages/DashboardPage'))
const AssetsPage          = lazy(() => import('@/pages/AssetsPage'))
const AssetDetailPage     = lazy(() => import('@/pages/AssetDetailPage'))
const DiscoveryPage       = lazy(() => import('@/pages/DiscoveryPage'))
const VulnerabilitiesPage = lazy(() => import('@/pages/VulnerabilitiesPage'))
const VulnerabilityDetail = lazy(() => import('@/pages/VulnerabilityDetailPage'))
const AssessmentPage      = lazy(() => import('@/pages/AssessmentPage'))
const RiskPage            = lazy(() => import('@/pages/RiskPage'))
const ActivityPage        = lazy(() => import('@/pages/ActivityPage'))
const HealthPage          = lazy(() => import('@/pages/HealthPage'))
const SettingsPage        = lazy(() => import('@/pages/SettingsPage'))
const NetworksPage        = lazy(() => import('@/pages/NetworksPage'))
const JobsPage            = lazy(() => import('@/pages/JobsPage'))

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard"              element={<DashboardPage />} />
        <Route path="/assets"                 element={<AssetsPage />} />
        <Route path="/assets/:id"             element={<AssetDetailPage />} />
        <Route path="/networks"               element={<NetworksPage />} />
        <Route path="/vulnerabilities"        element={<VulnerabilitiesPage />} />
        <Route path="/vulnerabilities/:id"    element={<VulnerabilityDetail />} />
        <Route path="/assessment"             element={<AssessmentPage />} />
        <Route path="/discovery"              element={<DiscoveryPage />} />
        <Route path="/jobs"                   element={<JobsPage />} />
        <Route path="/risk"                   element={<RiskPage />} />
        <Route path="/activity"               element={<ActivityPage />} />
        <Route path="/health"                 element={<HealthPage />} />
        <Route path="/settings"               element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
