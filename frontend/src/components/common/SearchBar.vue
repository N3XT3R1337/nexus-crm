<template>
  <div class="relative">
    <input v-model="query" type="text" placeholder="Search contacts, companies, deals... (Alt+S)"
      class="input-field pl-10" data-search-input @input="handleSearch" @focus="showResults = true"
      @blur="delayHideResults" />
    <svg class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
    <div v-if="showResults && results.length > 0"
      class="absolute top-full left-0 right-0 mt-1 card shadow-lg max-h-80 overflow-y-auto z-50">
      <div v-for="result in results" :key="result.entity_id"
        class="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer border-b border-gray-100 dark:border-gray-700 last:border-0"
        @mousedown="navigateTo(result)">
        <div class="flex items-center gap-3">
          <span class="badge" :class="typeClass(result.entity_type)">{{ result.entity_type }}</span>
          <div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">{{ result.title }}</p>
            <p v-if="result.subtitle" class="text-xs text-gray-500">{{ result.subtitle }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'
import type { SearchResult } from '@/types'

const router = useRouter()
const query = ref('')
const results = ref<SearchResult[]>([])
const showResults = ref(false)
let timeout: ReturnType<typeof setTimeout>

function delayHideResults() {
  setTimeout(() => showResults.value = false, 200)
}

function handleSearch() {
  clearTimeout(timeout)
  if (query.value.length < 2) {
    results.value = []
    return
  }
  timeout = setTimeout(async () => {
    try {
      const { data } = await apiClient.get('/search', { params: { q: query.value } })
      results.value = data.results
    } catch {
      results.value = []
    }
  }, 300)
}

function typeClass(type: string) {
  const classes: Record<string, string> = {
    contact: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    company: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    deal: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

function navigateTo(result: SearchResult) {
  const routes: Record<string, string> = {
    contact: '/contacts/',
    company: '/companies/',
    deal: '/deals/',
  }
  router.push((routes[result.entity_type] || '/') + result.entity_id)
  query.value = ''
  results.value = []
  showResults.value = false
}
</script>
