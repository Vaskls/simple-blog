<template>
    <div class="mt-10">
        <form @submit.prevent="handleSubmit">
        <div class="flex mx-3 flex-col my-1 items-center justify-center sm:mx-0">
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full p-8 transition-all text-white ">
                <h1 class="text-xl">Profile</h1>
                
                <div class="mt-4 flex flex-row place-content-start gap-5 mb-5"> 
                    <img
                        class="size-36 rounded-full object-cover"
                        :src=" 
                            newAvatar ? newAvatar : user.avatar
                        "
                    >
                    
                    <div class="flex flex-row gap-5 items-center">
                        <button @click="openPopup" class="bg-indigo-800 text-white py-2 px-4 rounded mt-2">Generate new avatar</button>
                    </div>
                </div>
                <h1 class="text-xl mb-6">Change username:</h1>
                <div class="flex md:flex-row md:my-2 gap-5 flex-col items-center">
                    <input v-model="newUsername" class="text-black inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 shadow border-2 border-indigo-900 rounded" placeholder="Username">
                    <p v-if="usernameError" class="text-red-500 text-sm">{{ usernameError }}</p>
                </div>
                <h1 class="text-xl mb-6 mt-6">Change password:</h1>
                <div class="flex md:flex-col md:my-2 gap-5 flex-col items-center">
                    <input v-model="oldPassword" class="text-black inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 shadow border-2 border-indigo-900 rounded" required placeholder="Current password" type="password">
                    <input v-model="newPassword" @input="validatePassword" class="text-black inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 shadow border-2 border-indigo-900 rounded" placeholder="New password" type="password">
                    <ul v-if="!isPasswordValid && newPassword.length > 0" class="text-red-500 text-sm list-disc ml-5">
                        <li v-if="!passwordLengthValid">Password must be at least 8 characters</li>
                        <li v-if="!passwordNumberValid">Password must contain at least one number</li>
                        <li v-if="!passwordSpecialValid">Password must contain at least one special symbol</li>
                        <li v-if="!passwordCapitalValid">Password must contain at least one capital letter</li>
                        <li v-if="passwordContainsUsernameError">Password must not contain username</li>
                    </ul>
                </div>
                <div class="flex justify-center mt-5">
                    <button class=" text-white py-2 px-4 rounded mt-2" :disable="disableSubmit" :class="!disableSubmit ? 'bg-indigo-800' : 'bg-indigo-400'">
                        Apply</button>
                </div>
            </div>
        </div>
        </form>
        <AvatarPopup :isOpen="popupOpened"/>
    
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import AvatarPopup from '~/components/elements/AvatarPopup.vue';
const { $listen } = useNuxtApp();
import passwordValidator from '~/api/passwordValidator.js';
import apiService from '~/api/api';

const props = defineProps({
    user: {
        type: Object,
        required: true
    }
});
const user = ref(props.user.value)
const popupOpened = ref(false)
const newAvatar = ref("")
const newUsername = ref('')

const usernameError = ref('');
const oldPassword = ref("")
const newPassword = ref("")
const passwordLengthValid = ref(false)
const passwordNumberValid = ref(false)
const passwordSpecialValid = ref(false)
const passwordCapitalValid = ref(false)
const isPasswordValid = ref(false);
const passwordContainsUsernameError = ref(false);

const disableSubmit = ref(true)

function openPopup() {
    popupOpened.value = true
}
const validatePassword = () => {
    console.log(ref.user)
    let validate = passwordValidator(newPassword, user.username)
    passwordLengthValid.value = validate.passwordLengthValid
    passwordNumberValid.value = validate.passwordNumberValid
    passwordSpecialValid.value = validate.passwordSpecialValid
    passwordCapitalValid.value = validate.passwordCapitalValid
    passwordContainsUsernameError.value = validate.passwordContainsUsernameError
    isPasswordValid.value = validate.isPasswordValid
};

watch( () => props.user, (newVal) => {
    user.value = newVal
}, { immediate : true})



$listen('popup:close', () => {
    console.log('Popup closed');
    popupOpened.value = false
});
$listen('popup:save', (avatar_value) => {
    popupOpened.value = false
    console.log("saved new", avatar_value)
    newAvatar.value = avatar_value
});

function checkUpdates() {
    return {
        avatar: newAvatar.value !== "",
        username: newUsername.value !== "",
        newPassword: newPassword.value !== "",
    }
}

watch(() => {
    const updatedFields = Object.entries(checkUpdates())
     .filter(([key, value]) => value === true)
     .map(([key]) => key);

    
    if (updatedFields.length > 0) {
        disableSubmit.value = false
    }
})


async function handleSubmit() {
    let data = {
        username: newUsername.value,
        avatar: newAvatar.value,
        password: oldPassword.value,
        newPassword: newPassword.value
    }
    try {
        let result = await apiService.put(
            "/user",
            data
        )
        alert("Profile updated!")
        

        window.location.href = '/settings'
    } catch (e) {
        // switch () {
        const err = e.response?.data?.detail
        if (err === "Invalid Credentials") {
            alert("Invalid credentials, request wasn't executed")
        } else if (err === "Username already exists") {
            alert("Username already exists, request wasn't executed")
        } else {
            alert("Error submitting request")
        }
    }
}

onMounted(() => {
    if (!props.user.username) {
        window.location.href = "/"
    }
})

</script>