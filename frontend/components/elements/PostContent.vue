<template>
    <div class="mb-6 border-2 border-gray-100 rounded-lg py-5 px-4" >
        {{ content }}
    </div>
</template>
  
<script setup>
const props = defineProps({
  content: {
    type: String,
    required: true
  }
})
</script>