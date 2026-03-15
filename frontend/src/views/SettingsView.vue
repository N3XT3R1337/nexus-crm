<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Settings</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Profile</h2>
          <form @submit.prevent="updateProfile" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">First Name</label>
                <input v-model="profile.first_name" type="text" class="input-field" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Last Name</label>
                <input v-model="profile.last_name" type="text" class="input-field" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone</label>
              <input v-model="profile.phone" type="tel" class="input-field" />
            </div>
            <button type="submit" class="btn-primary">Save Changes</button>
          </form>
        </div>

        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Change Password</h2>
          <form @submit.prevent="changePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Current Password</label>
              <input v-model="passwords.current" type="password" class="input-field" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">New Password</label>
              <input v-model="passwords.new_password" type="password" class="input-field" required minlength="6" />
            </div>
            <div v-if="passwordMessage" :class="['text-sm', passwordSuccess ? 'text-green-600' : 'text-red-600']">
              {{ passwordMessage }}
            </div>
            <button type="submit" class="btn-primary">Update Password</button>
          </form>
        </div>
      </div>

      <div class="space-y-6">
        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Appearance</h2>
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-700 dark:text-gray-300">Dark Mode</span>
            <button @click="toggleTheme"
              :class="['w-12 h-6 rounded-full transition-colors', isDark ? 'bg-primary-600' : 'bg-gray-300']">
              <span :class="['block w-5 h-5 rounded-full bg-white transform transition-transform', isDark ? 'translate-x-6' : 'translate-x-0.5']"></span>
            </button>
          </div>
        </div>

        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Account</h2>
          <div class="space-y-3 text-sm">
            <div><span class="text-gray-500">Email</span><p class="font-medium">{{ authStore.user?.email }}</p></div>
            <div><span class="text-gray-500">Role</span><p class="font-medium capitalize">{{ authStore.userRole.replace('_', ' ') }}</p></div>
            <div><span class="text-gray-500">Member Since</span><p class="font-medium">{{ authStore.user?.created_at ? new Date(authStore.user.created_at).toLocaleDateString() : '-' }}</p></div>
          </div>
        </div>

        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Keyboard Shortcuts</h2>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between"><span class="text-gray-500">Dashboard</span><kbd class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs">Alt+D</kbd></div>
            <div class="flex justify-between"><span class="text-gray-500">Contacts</span><kbd class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs">Alt+C</kbd></div>
            <div class="flex justify-between"><span class="text-gray-500">Companies</span><kbd class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs">Alt+O</kbd></div>
            <div class="flex justify-between"><span class="text-gray-500">Pipeline</span><kbd class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs">Alt+P</kbd></div>
            <div class="flex justify-between"><span class="text-gray-500">Search</span><kbd class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs">Alt+S</kbd></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import apiClient from '@/api/client'

const authStore = useAuthStore()
const { isDark, toggleTheme } = useTheme()

const profile = reactive({
  first_name: authStore.user?.first_name || '',
  last_name: authStore.user?.last_name || '',
  phone: authStore.user?.phone || '',
})

const passwords = reactive({ current: '', new_password: '' })
const passwordMessage = ref('')
const passwordSuccess = ref(false)

async function updateProfile() {
  await apiClient.put('/auth/me', profile)
  await authStore.fetchUser()
}

async function changePassword() {
  try {
    await apiClient.post('/auth/change-password', {
      current_password: passwords.current,
      new_password: passwords.new_password,
    })
    passwordMessage.value = 'Password updated successfully'
    passwordSuccess.value = true
    passwords.current = ''
    passwords.new_password = ''
  } catch (e: any) {
    passwordMessage.value = e.response?.data?.detail || 'Failed to change password'
    passwordSuccess.value = false
  }
}
</script>
