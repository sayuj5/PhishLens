import { useEffect, useRef, useState } from 'react'

const WS_URL = (import.meta.env.VITE_WS_URL ?? 'ws://localhost:8000') + '/api/ws/discovery'
const RECONNECT_DELAY_MS = 3000

export type WsMessage = {
  job_id?: number
  target?: string
  status?: string
  worker_id?: number
  [key: string]: unknown
}

export function useDiscoverySocket(onMessage: (msg: WsMessage) => void) {
  const wsRef = useRef<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)
  const reconnectTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const onMessageRef = useRef(onMessage)

  useEffect(() => {
    onMessageRef.current = onMessage
  }, [onMessage])

  useEffect(() => {
    function connect() {
      const ws = new WebSocket(WS_URL)
      wsRef.current = ws

      ws.onopen = () => {
        setConnected(true)
        if (reconnectTimer.current) clearTimeout(reconnectTimer.current)
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as WsMessage
          onMessageRef.current(data)
        } catch { /* ignore malformed messages */ }
      }

      ws.onerror = () => { ws.close() }

      ws.onclose = () => {
        setConnected(false)
        reconnectTimer.current = setTimeout(connect, RECONNECT_DELAY_MS)
      }
    }

    connect()
    return () => {
      if (reconnectTimer.current) clearTimeout(reconnectTimer.current)
      wsRef.current?.close()
    }
  }, [])

  return { connected }
}
