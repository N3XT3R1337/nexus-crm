<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Companies</h1>
      <button @click="showCreateModal = true" class="btn-primary">+ New Company</button>
    </div>

    <DataTable :columns="columns" :rows="store.companies" :total="store.total"
      :current-page="store.page" :per-page="store.perPage" :total-pages="store.pages"
      searchable @search="handleSearch" @sort="handleSort"
      @page-change="handlePageChange" @row-click="goToCompany">
      <template #filters>
        <select v-model="industryFilter" class="input-field w-40" @change="fetchData">
          <option value="">All Industries</option>
          <option v-for="ind in industries" :key="ind" :value="ind">{{ ind }}</option>
        </select>
      </template>

      <template #cell-name="{ row }">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-xs font-bold text-gray-600 dark:text-gray-300">
            {{ row.name?.[0] }}
          </div>
          <span class="font-medium">{{ row.name }}</span>
        </div>
      </template>

      <template #cell-revenue="{ value }">
        {{ value ? `$${Number(value).toLocaleString()}` : '-' }}
      </template>

      <template #rowActions="{ row }">
        <button @click.stop="deleteCompany(row.id)" class="text-red-500 hover:text-red-700 text-sm">Delete</button>
      </template>
    </DataTable>

    <Modal v-model="showCreateModal" title="New Company" size="lg">
      <FormBuilder :fields="formFields" submit-label="Create Company"
        @submit="handleCreate" @cancel="showCreateModal = false" />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCompaniesStore } from '@/stores/companies'
import DataTable from '@/components/common/DataTable.vue'
import Modal from '@/components/common/Modal.vue'
import FormBuilder from '@/components/common/FormBuilder.vue'

const router = useRouter()
const store = useCompaniesStore()
const showCreateModal = ref(false)
const industryFilter = ref('')
const searchQuery = ref('')

const industries = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Real Estate', 'Consulting', 'Media', 'Energy']

const columns = [
  { key: 'name', label: 'Company' },
  { key: 'industry', label: 'Industry' },
  { key: 'size', label: 'Size' },
  { key: 'revenue', label: 'Revenue' },
  { key: 'employee_count', label: 'Employees' },
  { key: 'city', label: 'City' },
  { key: 'created_at', label: 'Created' },
]

const formFields = [
  { key: 'name', label: 'Company Name', type: 'text', required: true },
  { key: 'domain', label: 'Domain', type: 'text' },
  { key: 'industry', label: 'Industry', type: 'select', options: industries.map(i => ({ value: i, label: i })) },
  { key: 'size', label: 'Size', type: 'select', options: ['1-10', '11-50', '51-200', '201-500', '501-1000', '1000+'].map(s => ({ value: s, label: s })) },
  { key: 'revenue', label: 'Revenue', type: 'number' },
  { key: 'phone', label: 'Phone', type: 'tel' },
  { key: 'email', label: 'Email', type: 'email' },
  { key: 'website', label: 'Website', type: 'url' },
  { key: 'description', label: 'Description', type: 'textarea' },
]

onMounted(() => fetchData())

async function fetchData() {
  await store.fetchCompanies({ search: searchQuery.value, industry: industryFilter.value })
}

function handleSearch(query: string) { searchQuery.value = query; store.page = 1; fetchData() }
function handleSort(key: string, order: string) { store.fetchCompanies({ sort_by: key, sort_order: order }) }
function handlePageChange(page: number) { store.page = page; fetchData() }
function goToCompany(row: any) { router.push(`/companies/${row.id}`) }
async function handleCreate(data: Record<string, any>) { await store.createCompany(data); showCreateModal.value = false }
async function deleteCompany(id: string) { if (confirm('Delete this company?')) await store.deleteCompany(id) }
</script>
