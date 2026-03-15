<template>
  <div v-if="company">
    <div class="flex items-center gap-4 mb-6">
      <button @click="$router.back()" class="btn-ghost">&larr; Back</button>
      <div class="flex-1">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ company.name }}</h1>
        <p class="text-gray-500">{{ company.industry }} &middot; {{ company.size }} employees</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Company Info</h2>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div><span class="text-gray-500">Domain</span><p class="font-medium">{{ company.domain || '-' }}</p></div>
            <div><span class="text-gray-500">Revenue</span><p class="font-medium">{{ company.revenue ? `$${company.revenue.toLocaleString()}` : '-' }}</p></div>
            <div><span class="text-gray-500">Phone</span><p class="font-medium">{{ company.phone || '-' }}</p></div>
            <div><span class="text-gray-500">Email</span><p class="font-medium">{{ company.email || '-' }}</p></div>
            <div><span class="text-gray-500">Website</span><p class="font-medium">{{ company.website || '-' }}</p></div>
            <div><span class="text-gray-500">Founded</span><p class="font-medium">{{ company.founded_year || '-' }}</p></div>
            <div class="col-span-2"><span class="text-gray-500">Address</span><p class="font-medium">{{ [company.address, company.city, company.state, company.country].filter(Boolean).join(', ') || '-' }}</p></div>
          </div>
        </div>

        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Contacts</h2>
          <div class="space-y-2">
            <div v-for="contact in contacts" :key="contact.id"
              class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg cursor-pointer"
              @click="$router.push(`/contacts/${contact.id}`)">
              <div class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-xs font-medium text-primary-600">
                {{ contact.first_name[0] }}{{ contact.last_name[0] }}
              </div>
              <div>
                <p class="text-sm font-medium">{{ contact.first_name }} {{ contact.last_name }}</p>
                <p class="text-xs text-gray-500">{{ contact.email }}</p>
              </div>
            </div>
            <p v-if="!contacts.length" class="text-sm text-gray-500">No contacts</p>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Deals</h2>
          <div class="space-y-2">
            <div v-for="deal in deals" :key="deal.id"
              class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
              @click="$router.push(`/deals/${deal.id}`)">
              <p class="text-sm font-medium">{{ deal.title }}</p>
              <p class="text-sm text-gray-500">${{ deal.value.toLocaleString() }}</p>
            </div>
            <p v-if="!deals.length" class="text-sm text-gray-500">No deals</p>
          </div>
        </div>

        <div v-if="company.description" class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Description</h2>
          <p class="text-sm text-gray-700 dark:text-gray-300">{{ company.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCompaniesStore } from '@/stores/companies'
import apiClient from '@/api/client'
import type { Contact, Deal } from '@/types'

const route = useRoute()
const store = useCompaniesStore()
const contacts = ref<Contact[]>([])
const deals = ref<Deal[]>([])
const company = computed(() => store.currentCompany)

onMounted(async () => {
  const id = route.params.id as string
  await store.fetchCompany(id)
  const [contactRes, dealRes] = await Promise.all([
    apiClient.get(`/companies/${id}/contacts`),
    apiClient.get(`/companies/${id}/deals`),
  ])
  contacts.value = contactRes.data
  deals.value = dealRes.data
})
</script>
