<template>
  <div v-if="contact">
    <div class="flex items-center gap-4 mb-6">
      <button @click="$router.back()" class="btn-ghost">&larr; Back</button>
      <div class="flex-1">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ contact.first_name }} {{ contact.last_name }}
        </h1>
        <p class="text-gray-500 dark:text-gray-400">{{ contact.job_title }} {{ contact.company?.name ? `at ${contact.company.name}` : '' }}</p>
      </div>
      <span :class="['badge', statusBadge]">{{ contact.status }}</span>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Details</h2>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div><span class="text-gray-500 dark:text-gray-400">Email</span><p class="font-medium">{{ contact.email || '-' }}</p></div>
            <div><span class="text-gray-500 dark:text-gray-400">Phone</span><p class="font-medium">{{ contact.phone || '-' }}</p></div>
            <div><span class="text-gray-500 dark:text-gray-400">Mobile</span><p class="font-medium">{{ contact.mobile || '-' }}</p></div>
            <div><span class="text-gray-500 dark:text-gray-400">Department</span><p class="font-medium">{{ contact.department || '-' }}</p></div>
            <div><span class="text-gray-500 dark:text-gray-400">Source</span><p class="font-medium">{{ contact.source }}</p></div>
            <div><span class="text-gray-500 dark:text-gray-400">Location</span><p class="font-medium">{{ [contact.city, contact.state, contact.country].filter(Boolean).join(', ') || '-' }}</p></div>
          </div>
        </div>

        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Activities</h2>
          <ActivityTimeline :activities="activities" />
        </div>
      </div>

      <div class="space-y-6">
        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Tags</h2>
          <div class="flex flex-wrap gap-2">
            <span v-for="tag in contact.tags" :key="tag.id"
              class="px-3 py-1 rounded-full text-xs text-white font-medium"
              :style="{ backgroundColor: tag.color }">{{ tag.name }}</span>
            <span v-if="!contact.tags?.length" class="text-sm text-gray-500">No tags</span>
          </div>
        </div>

        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Deals</h2>
          <div class="space-y-2">
            <div v-for="deal in deals" :key="deal.id"
              class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
              @click="$router.push(`/deals/${deal.id}`)">
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ deal.title }}</p>
              <p class="text-sm text-gray-500">${{ deal.value.toLocaleString() }}</p>
            </div>
            <p v-if="!deals.length" class="text-sm text-gray-500">No deals</p>
          </div>
        </div>

        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Notes</h2>
          <div class="space-y-3">
            <div v-for="note in notes" :key="note.id" class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p class="text-sm text-gray-700 dark:text-gray-300">{{ note.content }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ new Date(note.created_at).toLocaleDateString() }}</p>
            </div>
            <p v-if="!notes.length" class="text-sm text-gray-500">No notes</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useContactsStore } from '@/stores/contacts'
import apiClient from '@/api/client'
import ActivityTimeline from '@/components/activities/ActivityTimeline.vue'
import type { Activity, Deal, Note } from '@/types'

const route = useRoute()
const store = useContactsStore()
const activities = ref<Activity[]>([])
const deals = ref<Deal[]>([])
const notes = ref<Note[]>([])

const contact = computed(() => store.currentContact)

const statusBadge = computed(() => {
  const classes: Record<string, string> = {
    active: 'bg-green-100 text-green-800', lead: 'bg-blue-100 text-blue-800',
    customer: 'bg-purple-100 text-purple-800', inactive: 'bg-gray-100 text-gray-800',
  }
  return classes[contact.value?.status || ''] || 'bg-gray-100 text-gray-800'
})

onMounted(async () => {
  const id = route.params.id as string
  await store.fetchContact(id)
  const [actRes, dealRes, noteRes] = await Promise.all([
    apiClient.get(`/contacts/${id}/activities`),
    apiClient.get(`/contacts/${id}/deals`),
    apiClient.get(`/contacts/${id}/notes`),
  ])
  activities.value = actRes.data
  deals.value = dealRes.data
  notes.value = noteRes.data
})
</script>
