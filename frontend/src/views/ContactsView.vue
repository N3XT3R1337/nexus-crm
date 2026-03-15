<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Contacts</h1>
      <button @click="showCreateModal = true" class="btn-primary">+ New Contact</button>
    </div>

    <DataTable :columns="columns" :rows="store.contacts" :total="store.total"
      :current-page="store.page" :per-page="store.perPage" :total-pages="store.pages"
      selectable searchable @search="handleSearch" @sort="handleSort"
      @page-change="handlePageChange" @row-click="goToContact" @selection-change="selectedIds = $event">
      <template #filters>
        <select v-model="statusFilter" class="input-field w-36" @change="fetchData">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="lead">Lead</option>
          <option value="customer">Customer</option>
          <option value="inactive">Inactive</option>
          <option value="churned">Churned</option>
        </select>
      </template>

      <template #actions>
        <div v-if="selectedIds.length" class="flex gap-2">
          <button @click="handleBulkDelete" class="btn-danger text-sm">Delete ({{ selectedIds.length }})</button>
        </div>
      </template>

      <template #cell-first_name="{ row }">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-xs font-medium text-primary-600">
            {{ row.first_name?.[0] }}{{ row.last_name?.[0] }}
          </div>
          <span class="font-medium">{{ row.first_name }} {{ row.last_name }}</span>
        </div>
      </template>

      <template #cell-status="{ value }">
        <span :class="['badge', statusClass(value)]">{{ value }}</span>
      </template>

      <template #cell-tags="{ row }">
        <div class="flex gap-1">
          <span v-for="tag in (row.tags || []).slice(0, 2)" :key="tag.id"
            class="text-xs px-1.5 py-0.5 rounded-full text-white" :style="{ backgroundColor: tag.color }">
            {{ tag.name }}
          </span>
        </div>
      </template>

      <template #rowActions="{ row }">
        <button @click.stop="deleteContact(row.id)" class="text-red-500 hover:text-red-700 text-sm">Delete</button>
      </template>
    </DataTable>

    <Modal v-model="showCreateModal" title="New Contact" size="lg">
      <FormBuilder :fields="formFields" submit-label="Create Contact"
        @submit="handleCreate" @cancel="showCreateModal = false" />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useContactsStore } from '@/stores/contacts'
import DataTable from '@/components/common/DataTable.vue'
import Modal from '@/components/common/Modal.vue'
import FormBuilder from '@/components/common/FormBuilder.vue'

const router = useRouter()
const store = useContactsStore()

const showCreateModal = ref(false)
const statusFilter = ref('')
const searchQuery = ref('')
const selectedIds = ref<string[]>([])

const columns = [
  { key: 'first_name', label: 'Name' },
  { key: 'email', label: 'Email' },
  { key: 'phone', label: 'Phone' },
  { key: 'job_title', label: 'Job Title' },
  { key: 'status', label: 'Status' },
  { key: 'tags', label: 'Tags', sortable: false },
  { key: 'created_at', label: 'Created' },
]

const formFields = [
  { key: 'first_name', label: 'First Name', type: 'text', required: true },
  { key: 'last_name', label: 'Last Name', type: 'text', required: true },
  { key: 'email', label: 'Email', type: 'email' },
  { key: 'phone', label: 'Phone', type: 'tel' },
  { key: 'job_title', label: 'Job Title', type: 'text' },
  { key: 'department', label: 'Department', type: 'text' },
  { key: 'status', label: 'Status', type: 'select', options: [
    { value: 'lead', label: 'Lead' }, { value: 'active', label: 'Active' },
    { value: 'customer', label: 'Customer' }, { value: 'inactive', label: 'Inactive' },
  ]},
  { key: 'source', label: 'Source', type: 'select', options: [
    { value: 'website', label: 'Website' }, { value: 'referral', label: 'Referral' },
    { value: 'cold_call', label: 'Cold Call' }, { value: 'social_media', label: 'Social Media' },
    { value: 'email', label: 'Email' }, { value: 'event', label: 'Event' },
  ]},
]

function statusClass(status: string) {
  const classes: Record<string, string> = {
    active: 'bg-green-100 text-green-800', lead: 'bg-blue-100 text-blue-800',
    customer: 'bg-purple-100 text-purple-800', inactive: 'bg-gray-100 text-gray-800',
    churned: 'bg-red-100 text-red-800',
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

onMounted(() => fetchData())

async function fetchData() {
  await store.fetchContacts({ search: searchQuery.value, status: statusFilter.value })
}

function handleSearch(query: string) {
  searchQuery.value = query
  store.page = 1
  fetchData()
}

function handleSort(key: string, order: string) {
  store.fetchContacts({ sort_by: key, sort_order: order, search: searchQuery.value, status: statusFilter.value })
}

function handlePageChange(page: number) {
  store.page = page
  fetchData()
}

function goToContact(row: any) {
  router.push(`/contacts/${row.id}`)
}

async function handleCreate(data: Record<string, any>) {
  await store.createContact(data)
  showCreateModal.value = false
}

async function deleteContact(id: string) {
  if (confirm('Delete this contact?')) {
    await store.deleteContact(id)
  }
}

async function handleBulkDelete() {
  if (confirm(`Delete ${selectedIds.value.length} contacts?`)) {
    await store.bulkAction(selectedIds.value, 'delete')
    selectedIds.value = []
  }
}
</script>
