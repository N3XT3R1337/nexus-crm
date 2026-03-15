import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/client'
import type { Deal, DealStage, PaginatedResponse, PipelineStage } from '@/types'

export const useDealsStore = defineStore('deals', () => {
  const deals = ref<Deal[]>([])
  const currentDeal = ref<Deal | null>(null)
  const stages = ref<DealStage[]>([])
  const pipeline = ref<PipelineStage[]>([])
  const total = ref(0)
  const page = ref(1)
  const perPage = ref(25)
  const pages = ref(0)
  const loading = ref(false)

  async function fetchDeals(params: Record<string, any> = {}) {
    loading.value = true
    try {
      const { data } = await apiClient.get<PaginatedResponse<Deal>>('/deals', { params: { page: page.value, per_page: perPage.value, ...params } })
      deals.value = data.items
      total.value = data.total
      pages.value = data.pages
    } finally {
      loading.value = false
    }
  }

  async function fetchDeal(id: string) {
    const { data } = await apiClient.get<Deal>(`/deals/${id}`)
    currentDeal.value = data
    return data
  }

  async function fetchStages() {
    const { data } = await apiClient.get<DealStage[]>('/deals/stages')
    stages.value = data
  }

  async function fetchPipeline() {
    const { data } = await apiClient.get<PipelineStage[]>('/deals/pipeline')
    pipeline.value = data
  }

  async function createDeal(dealData: Record<string, any>) {
    const { data } = await apiClient.post<Deal>('/deals', dealData)
    deals.value.unshift(data)
    total.value++
    return data
  }

  async function updateDeal(id: string, dealData: Record<string, any>) {
    const { data } = await apiClient.put<Deal>(`/deals/${id}`, dealData)
    const index = deals.value.findIndex(d => d.id === id)
    if (index !== -1) deals.value[index] = data
    if (currentDeal.value?.id === id) currentDeal.value = data
    return data
  }

  async function deleteDeal(id: string) {
    await apiClient.delete(`/deals/${id}`)
    deals.value = deals.value.filter(d => d.id !== id)
    total.value--
  }

  async function transitionStage(dealId: string, stageId: string) {
    const { data } = await apiClient.post<Deal>(`/deals/${dealId}/transition`, { stage_id: stageId })
    const index = deals.value.findIndex(d => d.id === dealId)
    if (index !== -1) deals.value[index] = data
    return data
  }

  async function winDeal(dealId: string) {
    const { data } = await apiClient.post<Deal>(`/deals/${dealId}/win`, {})
    const index = deals.value.findIndex(d => d.id === dealId)
    if (index !== -1) deals.value[index] = data
    return data
  }

  async function loseDeal(dealId: string, reason: string) {
    const { data } = await apiClient.post<Deal>(`/deals/${dealId}/lose`, { lost_reason: reason })
    const index = deals.value.findIndex(d => d.id === dealId)
    if (index !== -1) deals.value[index] = data
    return data
  }

  return { deals, currentDeal, stages, pipeline, total, page, perPage, pages, loading, fetchDeals, fetchDeal, fetchStages, fetchPipeline, createDeal, updateDeal, deleteDeal, transitionStage, winDeal, loseDeal }
})
