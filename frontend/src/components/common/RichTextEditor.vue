<template>
  <div class="border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden">
    <div class="flex gap-1 p-2 bg-gray-50 dark:bg-gray-900 border-b border-gray-300 dark:border-gray-600">
      <button v-for="action in actions" :key="action.label" type="button" @click="action.handler"
        class="px-2 py-1 text-sm rounded hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
        :title="action.label">
        {{ action.icon }}
      </button>
    </div>
    <div ref="editorEl" contenteditable="true" :class="['p-3 min-h-[120px] focus:outline-none bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100']"
      @input="handleInput" v-html="modelValue">
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
const editorEl = ref<HTMLDivElement>()

const actions = [
  { label: 'Bold', icon: 'B', handler: () => document.execCommand('bold') },
  { label: 'Italic', icon: 'I', handler: () => document.execCommand('italic') },
  { label: 'Underline', icon: 'U', handler: () => document.execCommand('underline') },
  { label: 'List', icon: '\u2022', handler: () => document.execCommand('insertUnorderedList') },
  { label: 'Numbered', icon: '1.', handler: () => document.execCommand('insertOrderedList') },
  { label: 'Link', icon: '\u{1F517}', handler: () => {
    const url = prompt('Enter URL:')
    if (url) document.execCommand('createLink', false, url)
  }},
]

function handleInput() {
  if (editorEl.value) {
    emit('update:modelValue', editorEl.value.innerHTML)
  }
}
</script>
