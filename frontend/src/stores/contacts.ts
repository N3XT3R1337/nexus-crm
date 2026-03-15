import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/client'
import type { Contact, PaginatedResponse } from '@/types'

export const useContactsStore = defineStore('contacts', () => {
  const contacts = ref<Contact[]>([])
  const currentContact = ref<Contact | null>(null)
  const total = ref(0)
  const page = ref(1)
  const perPage = ref(25)
  const pages = ref(0)
  const loading = ref(false)

  async function fetchContacts(params: Record<string, any> = {}) {
    loading.value = true
    try {
      const { data } = await apiClient.get<PaginatedResponse<Contact>>('/contacts', { params: { page: page.value, per_page: perPage.value, ...params } })
      contacts.value = data.items
      total.value = data.total
      pages.value = data.pages
    } finally {
      loading.value = false
    }
  }

  async function fetchContact(id: string) {
    const { data } = await apiClient.get<Contact>(`/contacts/${id}`)
    currentContact.value = data
    return data
  }

  async function createContact(contactData: Record<string, any>) {
    const { data } = await apiClient.post<Contact>('/contacts', contactData)
    contacts.value.unshift(data)
    total.value++
    return data
  }

  async function updateContact(id: string, contactData: Record<string, any>) {
    const { data } = await apiClient.put<Contact>(`/contacts/${id}`, contactData)
    const index = contacts.value.findIndex(c => c.id === id)
    if (index !== -1) contacts.value[index] = data
    if (currentContact.value?.id === id) currentContact.value = data
    return data
  }

  async function deleteContact(id: string) {
    await apiClient.delete(`/contacts/${id}`)
    contacts.value = contacts.value.filter(c => c.id !== id)
    total.value--
  }

  async function bulkAction(ids: string[], action: string, value?: string) {
    await apiClient.post('/contacts/bulk', { ids, action, value })
    await fetchContacts()
  }

  return { contacts, currentContact, total, page, perPage, pages, loading, fetchContacts, fetchContact, createContact, updateContact, deleteContact, bulkAction }
})
