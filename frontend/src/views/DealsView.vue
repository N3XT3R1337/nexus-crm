<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Deals</h1>
      <div class="flex gap-3">
        <router-link to="/pipeline" class="btn-secondary">Pipeline View</router-link>
        <button @click="showCreateModal = true" class="btn-primary">+ New Deal</button>
      </div>
    </div>

    <DataTable :columns="columns" :rows="store.deals" :total="store.total"
      :current-page="store.page" :per-page="store.perPage" :total-pages="store.pages"
      searchable @search="handleSearch" @sort="handleSort"
      @page-change="handlePageChange" @row-click="goToDeal">
      <template #filters>
        <select v-model="statusFilter" class="input-field w-32" @change="fetchData">
          <option value="">All Status</option>
          <option value="open">Open</option>
          <option value="won">Won</option>
          <option value="lost">Lost</option>
        </select>
      </template>

      <template #cell-title="{ row }">
        <span class="font-medium">{{ row.title }}</span>
      </template>

      <template #cell-value="{ value }">
        <span class="font-bold">${{ Number(value).toLocaleString() }}</span>
      </template>

      <template #cell-status="{ value }">
        <span :class="['badge', value === 'won' ? 'bg-green-100 text-green-800' : value === 'lost' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800']">
          {{ value }}
        </span>
      </template>

      <template #cell-priority="{ value }">
        <span :class="['badge', value === 'critical' ? 'bg-red-100 text-red-800' : value === 'high' ? 'bg-orange-100 text-orange-800' : 'bg-gray-100 text-gray-800']">
          {{ value }}
        </span>
      </template>

      <template #rowActions="{ row }">
        <div class="flex gap-2">
          <button v-if="row.status === 'open'" @click.stop="handleWin(row.id)" class="text-green-600 hover:text-green-800 text-sm">Win</button>
          <button @click.stop="handleDelete(row.id)" class="text-red-500 hover:text-red-700 text-sm">Delete</button>
        </div>
      </template>
    </DataTable>

    <Modal v-model="showCreateModal" title="New Deal" size="lg">
      <FormBuilder :fields="formFields" submit-label="Create Deal"
        @submit="handleCreate" @cancel="showCreateModal = false" />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDealsStore } from '@/stores/deals'
import DataTable from '@/components/common/DataTable.vue'
import Modal from '@/components/common/Modal.vue'
import FormBuilder from '@/components/common/FormBuilder.vue'

const router = useRouter()
const store = useDealsStore()
const showCreateModal = ref(false)
const statusFilter = ref('')
const searchQuery = ref('')

const columns = [
  { key: 'title', label: 'Deal' },
  { key: 'value', label: 'Value' },
  { key: 'status', label: 'Status' },
  { key: 'priority', label: 'Priority' },
  { key: 'probability', label: 'Probability' },
  { key: 'created_at', label: 'Created' },
]

const formFields = [
  { key: 'title', label: 'Deal Title', type: 'text', required: true },
  { key: 'value', label: 'Value ($)', type: 'number', required: true },
  { key: 'priority', label: 'Priority', type: 'select', options: [
    { value: 'low', label: 'Low' }, { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }, { value: 'critical', label: 'Critical' },
  ]},
  { key: 'expected_close_date', label: 'Expected Close Date', type: 'date' },
  { key: 'description', label: 'Description', type: 'textarea' },
]

onMounted(() => { fetchData(); store.fetchStages() })

async function fetchData() {
  await store.fetchDeals({ search: searchQuery.value, status: statusFilter.value })
}

function handleSearch(query: string) { searchQuery.value = query; store.page = 1; fetchData() }
function handleSort(key: string, order: string) { store.fetchDeals({ sort_by: key, sort_order: order }) }
function handlePageChange(page: number) { store.page = page; fetchData() }
function goToDeal(row: any) { router.push(`/deals/${row.id}`) }
async function handleCreate(data: Record<string, any>) { await store.createDeal(data); showCreateModal.value = false }
async function handleWin(id: string) { await store.winDeal(id) }
async function handleDelete(id: string) { if (confirm('Delete this deal?')) await store.deleteDeal(id) }
</script>
