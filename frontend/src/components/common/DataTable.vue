<template>
  <div class="card overflow-hidden">
    <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between flex-wrap gap-4">
      <div class="flex items-center gap-3">
        <input v-if="searchable" v-model="searchQuery" type="text" placeholder="Search..."
          class="input-field w-64" @input="$emit('search', searchQuery)" />
        <slot name="filters" />
      </div>
      <div class="flex items-center gap-3">
        <span v-if="selectedRows.length" class="text-sm text-gray-500">{{ selectedRows.length }} selected</span>
        <slot name="actions" />
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-900/50">
          <tr>
            <th v-if="selectable" class="w-12 px-4 py-3">
              <input type="checkbox" :checked="allSelected" @change="toggleAll"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
            </th>
            <th v-for="col in columns" :key="col.key" class="table-header cursor-pointer select-none"
              @click="col.sortable !== false && handleSort(col.key)">
              <div class="flex items-center gap-1">
                {{ col.label }}
                <span v-if="sortBy === col.key" class="text-primary-500">
                  {{ sortOrder === 'asc' ? '\u25B2' : '\u25BC' }}
                </span>
              </div>
            </th>
            <th v-if="$slots.rowActions" class="table-header w-20">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="row in rows" :key="row.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer"
            @click="$emit('row-click', row)">
            <td v-if="selectable" class="w-12 px-4 py-3" @click.stop>
              <input type="checkbox" :checked="selectedRows.includes(row.id)" @change="toggleRow(row.id)"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
            </td>
            <td v-for="col in columns" :key="col.key" class="table-cell">
              <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
                {{ row[col.key] }}
              </slot>
            </td>
            <td v-if="$slots.rowActions" class="table-cell" @click.stop>
              <slot name="rowActions" :row="row" />
            </td>
          </tr>
          <tr v-if="rows.length === 0">
            <td :colspan="columns.length + (selectable ? 1 : 0) + ($slots.rowActions ? 1 : 0)"
              class="px-4 py-12 text-center text-gray-500 dark:text-gray-400">
              {{ emptyText }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="totalPages > 1" class="p-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
      <p class="text-sm text-gray-500">Showing {{ (currentPage - 1) * perPage + 1 }} to {{ Math.min(currentPage * perPage, total) }} of {{ total }}</p>
      <div class="flex gap-1">
        <button @click="$emit('page-change', currentPage - 1)" :disabled="currentPage <= 1"
          class="btn-ghost px-3 py-1 text-sm disabled:opacity-50">Prev</button>
        <button v-for="p in visiblePages" :key="p" @click="$emit('page-change', p)"
          :class="['px-3 py-1 text-sm rounded-lg', p === currentPage ? 'bg-primary-600 text-white' : 'btn-ghost']">
          {{ p }}
        </button>
        <button @click="$emit('page-change', currentPage + 1)" :disabled="currentPage >= totalPages"
          class="btn-ghost px-3 py-1 text-sm disabled:opacity-50">Next</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Column {
  key: string
  label: string
  sortable?: boolean
}

const props = withDefaults(defineProps<{
  columns: Column[]
  rows: any[]
  total?: number
  currentPage?: number
  perPage?: number
  totalPages?: number
  selectable?: boolean
  searchable?: boolean
  emptyText?: string
}>(), {
  total: 0, currentPage: 1, perPage: 25, totalPages: 1,
  selectable: false, searchable: true, emptyText: 'No records found',
})

const emit = defineEmits<{
  'row-click': [row: any]
  'search': [query: string]
  'sort': [key: string, order: string]
  'page-change': [page: number]
  'selection-change': [ids: string[]]
}>()

const searchQuery = ref('')
const sortBy = ref('')
const sortOrder = ref('desc')
const selectedRows = ref<string[]>([])

const allSelected = computed(() => props.rows.length > 0 && selectedRows.value.length === props.rows.length)

const visiblePages = computed(() => {
  const pages: number[] = []
  const start = Math.max(1, props.currentPage - 2)
  const end = Math.min(props.totalPages, start + 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

function handleSort(key: string) {
  if (sortBy.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = key
    sortOrder.value = 'asc'
  }
  emit('sort', sortBy.value, sortOrder.value)
}

function toggleAll() {
  selectedRows.value = allSelected.value ? [] : props.rows.map(r => r.id)
  emit('selection-change', selectedRows.value)
}

function toggleRow(id: string) {
  const index = selectedRows.value.indexOf(id)
  if (index >= 0) selectedRows.value.splice(index, 1)
  else selectedRows.value.push(id)
  emit('selection-change', selectedRows.value)
}
</script>
