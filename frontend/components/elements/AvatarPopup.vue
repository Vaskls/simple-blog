<template>
    <div v-if="isOpen" class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl p-8 w-full max-w-md relative">
            <button @click="close" class="absolute top-2 right-2 text-gray-500 hover:text-gray-700">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
            <h2 class="text-xl font-bold mb-4 text-black dark:text-white">Get a new one</h2>
            <div class="mb-4 flex justify-center">
                <img
                    class="size-36 rounded-full"
                    :src="newAvatar"
                >
            </div>
            <div class="flex justify-between items-end">
                <button @click="saveNew" class="bg-blue-500 text-white py-2 px-4 rounded mt-2">Save</button>
                <button :disabled="isLoading" @click="generateNewAvatar" 
                class="text-white py-2 px-4 rounded mt-2"
                :class="{
                    'bg-gray-500': isLoading,
                    'bg-gray-700': !isLoading
                }"
                >Generate new one</button>
            </div>
        </div>
    </div>
</template>

<script setup>

import { ref, watch } from 'vue';
import apiService from '~/api/api';
const { $event } = useNuxtApp()
const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    },
});
const newAvatar = ref('https://i.pinimg.com/originals/c0/27/be/c027bec07c2dc08b9df60921dfd539bd.webp')
const isLoading = ref(false)



async function generateNewAvatar() {
    isLoading.value = true
    try {
        let cat = await apiService.get("/cat") 
        console.log(cat)
        newAvatar.value = cat.url
    } catch {
    } finally {
        isLoading.value = false
    }
}
function saveNew() {
    $event('popup:save', newAvatar.value)
}
function close() {
    $event('popup:close')
}
</script>