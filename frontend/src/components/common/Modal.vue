<template>
  <Teleport to="body">
    <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center" data-modal @close="$emit('update:modelValue', false)">
      <div class="absolute inset-0 bg-black/50" @click="$emit('update:modelValue', false)"></div>
      <div :class="['relative bg-white dark:bg-gray-800 rounded-2xl shadow-xl', sizeClass]">
        <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">{{ title }}</h2>
          <button @click="$emit('update:modelValue', false)" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <slot />
        </div>
        <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  modelValue: boolean
  title: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
}>(), { size: 'md' })

defineEmits<{ 'update:modelValue': [value: boolean] }>()

const sizeClass = computed(() => {
  const sizes = { sm: 'w-full max-w-sm', md: 'w-full max-w-lg', lg: 'w-full max-w-2xl', xl: 'w-full max-w-4xl' }
  return sizes[props.size]
})
</script>
