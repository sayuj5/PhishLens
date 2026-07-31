import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function JobsPage() {
  const navigate = useNavigate()
  useEffect(() => {
    navigate('/dashboard', { replace: true })
  }, [navigate])
  return null
}
