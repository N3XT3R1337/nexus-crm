<template>
  <form @submit.prevent="$emit('submit', formData)" class="space-y-4">
    <div v-for="field in fields" :key="field.key" :class="field.colSpan === 2 ? '' : 'grid grid-cols-1'">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ field.label }}</label>
      <input v-if="field.type === 'text' || field.type === 'email' || field.type === 'number' || field.type === 'tel' || field.type === 'url'"
        v-model="formData[field.key]" :type="field.type" :placeholder="field.placeholder" :required="field.required"
        class="input-field" />
      <textarea v-else-if="field.type === 'textarea'" v-model="formData[field.key]"
        :placeholder="field.placeholder" :required="field.required" class="input-field" rows="3" />
      <select v-else-if="field.type === 'select'" v-model="formData[field.key]" :required="field.required" class="input-field">
        <option value="">Select {{ field.label }}</option>
        <option v-for="opt in field.options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
      <input v-else-if="field.type === 'date'" v-model="formData[field.key]" type="date" class="input-field" :required="field.required" />
    </div>
    <div class="flex justify-end gap-3 pt-4">
      <button type="button" class="btn-secondary" @click="$emit('cancel')">Cancel</button>
      <button type="submit" class="btn-primary" :disabled="loading">{{ submitLabel }}</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

interface FieldOption {
  value: string
  label: string
}

interface FormField {
  key: string
  label: string
  type: string
  placeholder?: string
  required?: boolean
  options?: FieldOption[]
  colSpan?: number
}

const props = withDefaults(defineProps<{
  fields: FormField[]
  initialData?: Record<string, any>
  submitLabel?: string
  loading?: boolean
}>(), { submitLabel: 'Save', loading: false })

defineEmits<{
  submit: [data: Record<string, any>]
  cancel: []
}>()

const formData = reactive<Record<string, any>>({})

watch(() => props.initialData, (data) => {
  if (data) Object.assign(formData, data)
}, { immediate: true })

props.fields.forEach(f => {
  if (!(f.key in formData)) formData[f.key] = ''
})
</script>
