<template>
  <div class="flex items-center gap-2">
    <input v-model="startDate" type="date" class="input-field" @change="emitChange" />
    <span class="text-gray-400">to</span>
    <input v-model="endDate" type="date" class="input-field" @change="emitChange" />
    <button v-for="preset in presets" :key="preset.label" @click="applyPreset(preset)"
      class="btn-ghost text-xs px-2 py-1">{{ preset.label }}</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  change: [start: string, end: string]
}>()

const startDate = ref('')
const endDate = ref('')

const presets = [
  { label: '7D', days: 7 },
  { label: '30D', days: 30 },
  { label: '90D', days: 90 },
]

function emitChange() {
  emit('change', startDate.value, endDate.value)
}

function applyPreset(preset: { days: number }) {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - preset.days)
  startDate.value = start.toISOString().split('T')[0]
  endDate.value = end.toISOString().split('T')[0]
  emitChange()
}
</script>
