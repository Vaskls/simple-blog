<template>
    <div class="mt-7">
        <div class="container px-4 mx-auto">
            <div class="max-w-lg mx-auto">
                <div class="text-center mb-6">
                <h2 class="text-3xl md:text-4xl font-extrabold">Sign in</h2>
                </div>
                <form @submit.prevent="submitForm">
                <div class="mb-6">
                    <label class="block mb-2 font-extrabold" for="">Username</label>
                    <input v-model="username" @input="checkIfInputsEmpty" class="inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded" type="Username" placeholder="Username">
                </div>
                <div class="mb-6">
                    <label class="block mb-2 font-extrabold" for="">Password</label>
                    <input v-model="password" @input="checkIfInputsEmpty" class="inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded" type="password" placeholder="**********">
                </div>
                <ul v-if="formError" class="text-red-500 text-sm list-disc ml-5">
                        <li>{{formErrorMessage}}</li>
                </ul>
                <div class="flex flex-wrap -mx-4 mb-6 items-center justify-between">
                    
                    
                </div>
                <button :disabled="disableSubmit" :class="!disableSubmit ? 'bg-indigo-800' : 'bg-indigo-400'" class="inline-block w-full py-4 px-6 mb-6 text-center text-lg leading-6 text-white font-extrabold hover:bg-indigo-900 border-3 border-indigo-900 shadow rounded transition duration-200">Sign in</button>
                <p class="text-center font-extrabold">Don't have an account? <a class="text-black-500 underline"
                    href="/signup">Sign up</a></p>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import apiService from '~/api/api.js';
const { $event } = useNuxtApp()

const username = ref('');
const password = ref('');

const disableSubmit = ref(true);
const formError = ref(false)
const formErrorMessage = ref('')

const checkIfInputsEmpty = () => {
    formError.value = false
    disableSubmit.value = !(password.value.length > 0 && username.value.length > 0)
}

const submitForm = async () =>  {
    try {
        const result = await apiService.sendAuthRequest(username.value, password.value);
        if (result.data.access_token) {
            localStorage.setItem('access_token', result.data.access_token)
            window.location.href = "/"
        }
        
    } catch (e) {
        const err = e.response?.data?.detail
        if (err === "Invalid Credentials") {
            formError.value = true
            formErrorMessage.value = "Invalid Credentials"
        } else {
            formError.value = true
            formErrorMessage.value = "Error submittings form"
        }
    }
};



</script>