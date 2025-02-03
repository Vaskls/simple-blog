<template>
  <div class="border rounded p-4 mb-2 flex flex-row">
    <div class="flex items-center">
      <img :src="comment.author.avatar" alt="Author Avatar" class="w-10 h-10 rounded-full mr-2">
    </div>
    <div class="flex flex-col">
      <div class="flex items-center mb-2">
          <div class="font-semibold">{{ comment.author.username }}</div>
          <div class="text-gray-500 text-sm ml-2">{{ formattedDate }}</div>
      </div>
      <div>{{ comment.contents }}</div>
    </div>
      
  </div>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
});

const formattedDate = computed(() => {
  const date = new Date(props.comment.created);
  return date.toLocaleDateString(undefined, {
     year: 'numeric',
     month: 'long',
     day: 'numeric',
     hour: 'numeric',
     minute: 'numeric'
   });
})

</script>