import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/client'
import type { Company, PaginatedResponse } from '@/types'

export const useCompaniesStore = defineStore('companies', () => {
  const companies = ref<Company[]>([])
  const currentCompany = ref<Company | null>(null)
  const total = ref(0)
  const page = ref(1)
  const perPage = ref(25)
  const pages = ref(0)
  const loading = ref(false)

  async function fetchCompanies(params: Record<string, any> = {}) {
    loading.value = true
    try {
      const { data } = await apiClient.get<PaginatedResponse<Company>>('/companies', { params: { page: page.value, per_page: perPage.value, ...params } })
      companies.value = data.items
      total.value = data.total
      pages.value = data.pages
    } finally {
      loading.value = false
    }
  }

  async function fetchCompany(id: string) {
    const { data } = await apiClient.get<Company>(`/companies/${id}`)
    currentCompany.value = data
    return data
  }

  async function createCompany(companyData: Record<string, any>) {
    const { data } = await apiClient.post<Company>('/companies', companyData)
    companies.value.unshift(data)
    total.value++
    return data
  }

  async function updateCompany(id: string, companyData: Record<string, any>) {
    const { data } = await apiClient.put<Company>(`/companies/${id}`, companyData)
    const index = companies.value.findIndex(c => c.id === id)
    if (index !== -1) companies.value[index] = data
    if (currentCompany.value?.id === id) currentCompany.value = data
    return data
  }

  async function deleteCompany(id: string) {
    await apiClient.delete(`/companies/${id}`)
    companies.value = companies.value.filter(c => c.id !== id)
    total.value--
  }

  return { companies, currentCompany, total, page, perPage, pages, loading, fetchCompanies, fetchCompany, createCompany, updateCompany, deleteCompany }
})
