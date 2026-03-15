<template>
  <div class="flex flex-wrap gap-2 p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 min-h-[42px]">
    <span v-for="tag in selectedTags" :key="tag.id"
      class="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium text-white"
      :style="{ backgroundColor: tag.color }">
      {{ tag.name }}
      <button @click="removeTag(tag.id)" class="hover:opacity-75">&times;</button>
    </span>
    <input v-model="input" type="text" :placeholder="selectedTags.length ? '' : placeholder"
      class="flex-1 min-w-[120px] outline-none bg-transparent text-sm text-gray-900 dark:text-gray-100"
      @input="handleInput" @keydown.backspace="handleBackspace" />
    <div v-if="showSuggestions && filteredTags.length > 0"
      class="absolute top-full left-0 right-0 mt-1 card shadow-lg max-h-40 overflow-y-auto z-50">
      <div v-for="tag in filteredTags" :key="tag.id"
        class="px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer flex items-center gap-2"
        @mousedown="addTag(tag)">
        <span class="w-3 h-3 rounded-full" :style="{ backgroundColor: tag.color }"></span>
        {{ tag.name }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Tag } from '@/types'

const props = defineProps<{
  availableTags: Tag[]
  modelValue: Tag[]
  placeholder?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [tags: Tag[]]
}>()

const input = ref('')
const showSuggestions = ref(false)

const selectedTags = computed(() => props.modelValue)

const filteredTags = computed(() => {
  const selectedIds = selectedTags.value.map(t => t.id)
  return props.availableTags
    .filter(t => !selectedIds.includes(t.id))
    .filter(t => t.name.toLowerCase().includes(input.value.toLowerCase()))
})

function addTag(tag: Tag) {
  emit('update:modelValue', [...selectedTags.value, tag])
  input.value = ''
  showSuggestions.value = false
}

function removeTag(id: string) {
  emit('update:modelValue', selectedTags.value.filter(t => t.id !== id))
}

function handleInput() {
  showSuggestions.value = input.value.length > 0
}

function handleBackspace() {
  if (!input.value && selectedTags.value.length > 0) {
    const last = selectedTags.value[selectedTags.value.length - 1]
    removeTag(last.id)
  }
}
</script>
