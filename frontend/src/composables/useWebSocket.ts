import { ref, onUnmounted } from 'vue'

export function useWebSocket() {
  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const lastMessage = ref<any>(null)

  function connect() {
    const token = localStorage.getItem('access_token')
    if (!token) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    ws.value = new WebSocket(`${protocol}//${window.location.host}/ws/${token}`)

    ws.value.onopen = () => {
      isConnected.value = true
    }

    ws.value.onmessage = (event) => {
      lastMessage.value = JSON.parse(event.data)
    }

    ws.value.onclose = () => {
      isConnected.value = false
      setTimeout(connect, 5000)
    }
  }

  function disconnect() {
    ws.value?.close()
    ws.value = null
    isConnected.value = false
  }

  function send(data: any) {
    if (ws.value?.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify(data))
    }
  }

  onUnmounted(disconnect)

  return { isConnected, lastMessage, connect, disconnect, send }
}
