<template>
  <div>
    <div v-if="isLoading">
        <!-- Loading indicator, use a component or an icon -->
        <div class="loading-overlay">
            <div class="loader"></div>
        </div>
    </div>
    <div v-else>
      <AppHeader  :isLoggedIn="isLoggedIn" :user="user"/>
        <component :is="currentTemplate" :user="user"/>
    </div>
  </div>
</template>



<script setup>
import { ref, watch, onMounted, shallowRef } from 'vue';
import { useNuxtApp, useRouter } from '#app';
const { $listen } = useNuxtApp();
import apiService from '~/api/api.js';

import AppHeader from './components/elements/AppHeader.vue';

import LoginForm from './components/pages/LoginForm.vue';
import SignupForm from './components/pages/SignupForm.vue';
import Dashboard from './components/pages/Dashboard.vue';
import Post from './components/pages/Post.vue';
import PostForm from './components/pages/PostForm.vue';
import Stats from './components/pages/Stats.vue';
import Settings from './components/pages/Settings.vue';
import Profile from './components/pages/Profile.vue';
import PageNotFound from './components/pages/PageNotFound.vue';

const router = useRouter();

const isLoggedIn = ref(false);
let user = ref({});

const routeComponents = {
    '/': Dashboard,
    '/signin': LoginForm,
    '/signup': SignupForm,
    '/newpost': PostForm,
    '/stats': Stats,
    '/settings': Settings,
    '/profile': Profile,
    '*': PageNotFound,
};

const currentTemplate = shallowRef(routeComponents['*']);
const isLoading = ref(true); // Initially, the page is loading

const resolveComponent = (path) => {
    if (path.startsWith('/post/')) {
        return Post;
    }
    return routeComponents[path] || routeComponents['*'];
};


onMounted(async () => {
    try{
        const user_data = await apiService.getMe();
        if (user_data) {
            localStorage.setItem("avatar", user_data.avatar)
            localStorage.setItem("username", user_data.username)
            isLoggedIn.value = true;
            user.value = user_data
        }
    } catch(error) {
        user.value = {}
        isLoggedIn.value = false
    } finally {
        isLoading.value = false;
    }


    $listen(['user:signedin', 'user:registered'], (user) => {
        console.log('A user was registered!', user);
    });
    if(!router?.currentRoute?.value?.path) return;
    currentTemplate.value = resolveComponent(router.currentRoute.value.path);
});

watch(
    () => router?.currentRoute?.value?.path,
    async (newPath) => {
      isLoading.value = true
      try {
        if (newPath) {
          currentTemplate.value = resolveComponent(newPath);
        }
      } finally {
        isLoading.value = false;
      }
    }
);
</script>
<style scoped>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999; 
}

.loader {
    border: 8px solid #f3f3f3;
    border-top: 8px solid #236ea0;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>