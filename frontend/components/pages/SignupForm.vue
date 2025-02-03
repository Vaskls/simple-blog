<template>
    <div class="mt-7">
        <div class="container px-4 mx-auto">
            <div class="max-w-lg mx-auto">
                <div class="text-center mb-6">
                <h2 class="text-3xl md:text-4xl font-extrabold">Sign up</h2>
                </div>
                <form @submit.prevent="submitForm">
                <div class="mb-6">
                    <label class="block mb-2 font-extrabold" for="">Username</label>
                    <input v-model="username" @blur="checkUsernameAvailability" class="inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded" type="Username" placeholder="Username">
                    <p v-if="usernameError" class="text-red-500 text-sm">{{ usernameError }}</p>
                </div>
                <div class="mb-6">
                    <label class="block mb-2 font-extrabold" for="">Password</label>
                    <input v-model="password" @input="validatePassword" class="inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded" type="password" placeholder="**********">
                    <ul v-if="!isPasswordValid && password.length > 0" class="text-red-500 text-sm list-disc ml-5">
                        <li v-if="!passwordLengthValid">Password must be at least 8 characters</li>
                        <li v-if="!passwordNumberValid">Password must contain at least one number</li>
                        <li v-if="!passwordSpecialValid">Password must contain at least one special symbol</li>
                        <li v-if="!passwordCapitalValid">Password must contain at least one capital letter</li>
                        <li v-if="passwordContainsUsernameError">Password must not contain username</li>
                    </ul>
                </div>
                <div class="mb-6">
                    <label class="block mb-2 font-extrabold" for="">Repeat password</label>
                    <input v-model="passwordRepeat" @input="validatePasswordRepeat" @blur="validatePasswordRepeat" class="inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded" type="password" placeholder="**********">
                    <p v-if="passwordRepeatError" class="text-red-500 text-sm">{{ passwordRepeatError }}</p>
                </div>
                
                <div class="flex flex-wrap -mx-4 mb-6 items-center justify-between">
                    
                    
                </div>
                <p v-if="isLoading" class="text-green-500 text-sm">Loading....</p>
                <p v-if="isError" class="text-red-500 text-sm">Error: {{ errormessage }}</p>
                <p v-if="isSuccess" class="text-green-500 text-lg">Account created!</p>
                <button :disabled="disableSubmit" :class="!disableSubmit ? 'bg-indigo-800' : 'bg-indigo-400'" class="inline-block w-full py-4 px-6 mb-6 text-center text-lg leading-6 text-white font-extrabold hover:bg-indigo-900 border-3 shadow rounded transition duration-200">Sign up</button>
                <p class="text-center font-extrabold">Have an account already? <a class="text-black-500 underline"
                    href="/signin">Sign in</a></p>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>


import { ref, computed } from 'vue';
import apiService from '~/api/api.js';
import passwordValidator from '~/api/passwordValidator.js';

const username = ref('');
const password = ref('');
const passwordRepeat = ref('');
const usernameError = ref('');
const passwordRepeatError = ref('');
const disableSubmit = ref(true);
const isLoading = ref(false)
const isSuccess = ref(false)
const isError = ref(false)
const errormessage = ref("")
const passwordContainsUsernameError = ref(false);

const isPasswordValid = ref(false);
const passwordLengthValid = ref(false)
const passwordNumberValid = ref(false)
const passwordSpecialValid = ref(false)
const passwordCapitalValid = ref(false)



const validatePassword = () => {
    let validate = passwordValidator(password, username) 
    passwordLengthValid.value = validate.passwordLengthValid
    passwordNumberValid.value = validate.passwordNumberValid
    passwordSpecialValid.value = validate.passwordSpecialValid
    passwordCapitalValid.value = validate.passwordCapitalValid
    passwordContainsUsernameError.value = validate.passwordContainsUsernameError
    isPasswordValid.value = validate.isPasswordValid
    disableSubmit.value = !isFormValid.value
};



const validatePasswordRepeat = () => {
  if (password.value !== passwordRepeat.value) {
    passwordRepeatError.value = "Passwords do not match";
  } else {
    passwordRepeatError.value = "";
  }
  disableSubmit.value = !isFormValid.value
};




const checkUsernameAvailability = async () => {
    
    var result = await apiService.checkUsernameAvailability(username.value)
    if (result.exists) {
        usernameError.value = "Username is already taken.";
    } else {
        usernameError.value = ""
    }
    
    disableSubmit.value = !isFormValid.value
}


const isFormValid = computed(() => {
    return isPasswordValid.value && usernameError.value === "" && passwordRepeatError.value === "" && username.value !== "";
})



const submitForm = async () => {
    
    if (isFormValid.value) {
        isError.value = false
        isLoading.value = true
        try {
            await apiService.post(
                "/user",
                {
                    username: username.value,
                    password: password.value
                }
            )
            isSuccess.value = true
            const result = await apiService.sendAuthRequest(username.value, password.value)
            localStorage.setItem('access_token', result.data.access_token)
            window.location.href = "/"
        } catch {
            isError.value = true
            errormessage.value = "Error submitting the form"
        } finally {
            isLoading.value = false
        }
    } else {
        alert("Form has errors")
    }
};
</script>