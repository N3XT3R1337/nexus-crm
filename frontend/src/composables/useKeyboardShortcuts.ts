import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export function useKeyboardShortcuts() {
  const router = useRouter()

  function handleKeydown(e: KeyboardEvent) {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return

    if (e.altKey) {
      switch (e.key) {
        case 'd':
          e.preventDefault()
          router.push('/dashboard')
          break
        case 'c':
          e.preventDefault()
          router.push('/contacts')
          break
        case 'o':
          e.preventDefault()
          router.push('/companies')
          break
        case 'p':
          e.preventDefault()
          router.push('/deals')
          break
        case 'a':
          e.preventDefault()
          router.push('/activities')
          break
        case 's':
          e.preventDefault()
          document.querySelector<HTMLInputElement>('[data-search-input]')?.focus()
          break
      }
    }

    if (e.key === 'Escape') {
      const modal = document.querySelector('[data-modal]')
      if (modal) {
        modal.dispatchEvent(new CustomEvent('close'))
      }
    }
  }

  onMounted(() => document.addEventListener('keydown', handleKeydown))
  onUnmounted(() => document.removeEventListener('keydown', handleKeydown))
}
