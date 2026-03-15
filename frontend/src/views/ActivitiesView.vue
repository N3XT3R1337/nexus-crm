<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Activities</h1>
      <button @click="showCreateModal = true" class="btn-primary">+ New Activity</button>
    </div>

    <DataTable :columns="columns" :rows="activities" :total="total"
      :current-page="page" :per-page="25" :total-pages="pages"
      searchable @search="handleSearch" @page-change="handlePageChange">
      <template #filters>
        <select v-model="typeFilter" class="input-field w-36" @change="fetchData">
          <option value="">All Types</option>
          <option v-for="t in activityTypes" :key="t" :value="t">{{ t }}</option>
        </select>
        <select v-model="completedFilter" class="input-field w-36" @change="fetchData">
          <option value="">All Status</option>
          <option value="false">Pending</option>
          <option value="true">Completed</option>
        </select>
      </template>

      <template #cell-type="{ value }">
        <span class="badge bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 capitalize">{{ value }}</span>
      </template>

      <template #cell-completed="{ value, row }">
        <button @click.stop="toggleComplete(row)" :class="['w-5 h-5 rounded border-2', value ? 'bg-green-500 border-green-500 text-white' : 'border-gray-300 dark:border-gray-600']">
          <span v-if="value" class="text-xs">&#10003;</span>
        </button>
      </template>

      <template #cell-due_date="{ value }">
        <span :class="[value && new Date(value) < new Date() ? 'text-red-500' : '']">
          {{ value ? new Date(value).toLocaleDateString() : '-' }}
        </span>
      </template>

      <template #rowActions="{ row }">
        <button @click.stop="deleteActivity(row.id)" class="text-red-500 hover:text-red-700 text-sm">Delete</button>
      </template>
    </DataTable>

    <Modal v-model="showCreateModal" title="New Activity">
      <FormBuilder :fields="formFields" submit-label="Create Activity"
        @submit="handleCreate" @cancel="showCreateModal = false" />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'
import DataTable from '@/components/common/DataTable.vue'
import Modal from '@/components/common/Modal.vue'
import FormBuilder from '@/components/common/FormBuilder.vue'
import type { Activity } from '@/types'

const activities = ref<Activity[]>([])
const total = ref(0)
const page = ref(1)
const pages = ref(0)
const showCreateModal = ref(false)
const typeFilter = ref('')
const completedFilter = ref('')
const activityTypes = ['call', 'email', 'meeting', 'task', 'note', 'follow_up', 'demo', 'proposal']

const columns = [
  { key: 'type', label: 'Type' },
  { key: 'subject', label: 'Subject' },
  { key: 'completed', label: 'Done' },
  { key: 'due_date', label: 'Due Date' },
  { key: 'created_at', label: 'Created' },
]

const formFields = [
  { key: 'type', label: 'Type', type: 'select', required: true, options: activityTypes.map(t => ({ value: t, label: t })) },
  { key: 'subject', label: 'Subject', type: 'text', required: true },
  { key: 'description', label: 'Description', type: 'textarea' },
  { key: 'due_date', label: 'Due Date', type: 'date' },
  { key: 'duration_minutes', label: 'Duration (min)', type: 'number' },
  { key: 'location', label: 'Location', type: 'text' },
]

onMounted(() => fetchData())

async function fetchData() {
  const params: Record<string, any> = { page: page.value, per_page: 25 }
  if (typeFilter.value) params.type = typeFilter.value
  if (completedFilter.value) params.completed = completedFilter.value
  const { data } = await apiClient.get('/activities', { params })
  activities.value = data.items
  total.value = data.total
  pages.value = data.pages
}

function handleSearch(q: string) { page.value = 1; fetchData() }
function handlePageChange(p: number) { page.value = p; fetchData() }

async function handleCreate(data: Record<string, any>) {
  await apiClient.post('/activities', data)
  showCreateModal.value = false
  fetchData()
}

async function toggleComplete(row: Activity) {
  if (row.completed) {
    await apiClient.put(`/activities/${row.id}`, { completed: false })
  } else {
    await apiClient.post(`/activities/${row.id}/complete`)
  }
  fetchData()
}

async function deleteActivity(id: string) {
  if (confirm('Delete this activity?')) {
    await apiClient.delete(`/activities/${id}`)
    fetchData()
  }
}
</script>
