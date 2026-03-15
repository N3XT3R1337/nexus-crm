import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/client'
import type { User, TokenResponse } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))

  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || '')
  const fullName = computed(() => user.value ? `${user.value.first_name} ${user.value.last_name}` : '')

  async function login(email: string, password: string) {
    const { data } = await apiClient.post<TokenResponse>('/auth/login', { email, password })
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
  }

  async function register(email: string, password: string, firstName: string, lastName: string) {
    const { data } = await apiClient.post<TokenResponse>('/auth/register', {
      email, password, first_name: firstName, last_name: lastName,
    })
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
  }

  async function fetchUser() {
    try {
      const { data } = await apiClient.get<User>('/auth/me')
      user.value = data
    } catch {
      logout()
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  function hasPermission(permission: string): boolean {
    const role = user.value?.role
    if (!role) return false

    const rolePerms: Record<string, string[]> = {
      super_admin: ['*'],
      admin: ['contacts:*', 'companies:*', 'deals:*', 'activities:*', 'notes:*', 'reports:*', 'users:read', 'users:write', 'settings:*', 'webhooks:*', 'api_keys:*', 'audit:*', 'tags:*', 'dashboard:*', 'email_templates:*'],
      manager: ['contacts:*', 'companies:*', 'deals:*', 'activities:*', 'notes:*', 'reports:*', 'users:read', 'tags:*', 'dashboard:*', 'email_templates:*'],
      sales_rep: ['contacts:read', 'contacts:write', 'companies:read', 'companies:write', 'deals:*', 'activities:*', 'notes:*', 'tags:read', 'tags:write', 'dashboard:*', 'email_templates:read'],
      viewer: ['contacts:read', 'companies:read', 'deals:read', 'activities:read', 'notes:read', 'tags:read', 'dashboard:read', 'reports:read'],
    }

    const perms = rolePerms[role] || []
    if (perms.includes('*')) return true

    return perms.some(p => {
      if (p.endsWith(':*')) {
        return permission.startsWith(p.replace(':*', ':'))
      }
      return p === permission
    })
  }

  return { user, token, isAuthenticated, userRole, fullName, login, register, fetchUser, logout, hasPermission }
})
