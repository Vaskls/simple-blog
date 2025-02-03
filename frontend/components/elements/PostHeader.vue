<template>
    <div class="flex items-center mb-4">
      <img :src="author.avatar" alt="Author Avatar" class="w-10 h-10 rounded-full mr-2">
      <div>
        <div class="font-bold">{{ title }}</div>
        <div class="font-semibold">{{ author.username }}</div>
        <div class="text-gray-500 text-sm">{{ formattedDate }}</div>
      </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  author: {
    type: Object,
    required: true,
  },
  createdAt: {
    type: String,
    required: true
  }
});


const formattedDate = computed(() => {
  const date = new Date(props.createdAt);
  return date.toLocaleDateString(undefined, {
     year: 'numeric',
     month: 'long',
     day: 'numeric'
   });
})


</script>