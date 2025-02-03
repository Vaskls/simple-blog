<template>
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold mb-8 text-gray-800">Create a New Blog Post</h1>

        <form @submit.prevent="handleSubmit">
        <div class="mb-6">
            <label for="title" class="block text-gray-700 text-sm font-bold mb-2">
            Post Title
            </label>
            <input
            type="text"
            id="title"
            v-model="title"
            placeholder="Enter your post title"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
            />
        </div>

        <div class="mb-6">
            <label for="content" class="block text-gray-700 text-sm font-bold mb-2">
            Post Content
            </label>
            <textarea
            id="content"
            v-model="content"
            rows="8"
            placeholder="Write post contents here..."
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
            ></textarea>
        </div>

        <div class="flex justify-end">
            <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
            Publish Post
            </button>
        </div>
        </form>
    </div>
</template>

<script setup>
import {ref} from 'vue'
import apiService from '~/api/api.js';
let title = ref('')
let content = ref('')
// IF NOT ADMIN RELOCATE TO notfound

async function handleSubmit() {
    console.log("Submit clicked")

    console.log(title.value, content.value)
    await apiService.post("/post/", {
        header: title.value,
        contents: content.value,
        iscomment: false
    })
    alert("Post created!")
    window.location.href = "/"
}
</script>