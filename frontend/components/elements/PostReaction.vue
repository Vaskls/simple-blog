<template>
    <div class="flex items-center space-x-4 mb-4">
      <button @click="like" :class="{
          'text-blue-500' : current_reaction === true
      }"
          class="hover:text-blue-600 transition-colors">
        <span class="font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 inline-block">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.099 3.75 3 5.765 3 8.25c0 7.229 9 12 9 12s9-4.771 9-12Z" />
            </svg>
            {{ likes }}
        </span>
      </button>
      <button @click="dislike" :class="{
          'text-red-500' : current_reaction === false, 
      }" class="hover:text-red-600 transition-colors">
          <span class="font-medium">
               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 inline-block">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
             {{ dislikes }}
        </span>
      </button>
    </div>
</template>
  
<script setup>
import { ref, watch } from "vue";
import apiService from "~/api/api.js"
const { $event } = useNuxtApp()
const props = defineProps({
  likes: {
    type: Number,
    required: true,
  },
  dislikes: {
    type: Number,
    required: true,
  },
  post_id: {
    type: Number,
    required: true
  },
  current_reaction: {
    type: Boolean,
    default: undefined,
    required: false
  }
})



async function sendReactionRequest(value) {
  try {
    await apiService.post("/reaction/", {
      post_id: props.post_id,
      value: value
    })
    return true
  } catch {
    return alert("You have to be authorised to perform this action")
  }
}

async function like() {
  const result = await sendReactionRequest(true)
  if (result) {
    $event('reaction:add', true)
  }
}
async function dislike() {
  const result = await sendReactionRequest(false)
  if (result) {
    $event('reaction:add', false)
  }
}
</script>