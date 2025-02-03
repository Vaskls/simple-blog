

<script setup>
import { ref } from 'vue';



const props = defineProps({
    isLoggedIn: {
        type: Boolean,
        default: false
    },
    notifications: {
        type: Array,
        required: false,
        default: () => [] ,
        validator: (value) => {
            if (!Array.isArray(value)) return false
            return value.every((element) => typeof element === 'string')
        },
    },
    user: {
        type: Object,
        required: false
    },
});
function logOut() {
  localStorage.clear()
  window.location.reload();
}





const mobileMenuOpen = ref(false);
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const profileDropdownOpen = ref(false);
const toggleProfileDropdown = () => {
    profileDropdownOpen.value = !profileDropdownOpen.value
}
onMounted(() => {
  document.addEventListener('click', function (event) {
    
    if (event.target.id !== "profile-btn") {
        profileDropdownOpen.value = false
    } 
    if (event.target.id !== "mobile-menu-button") {
        mobileMenuOpen.value = false
    } 
  });
});


</script>


<template>
    <header class="app-header">
      <nav class="bg-gray-800">
        <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
          <div class="relative flex h-16 items-center justify-between">
            <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
              <button
                type="button"
                class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                aria-controls="mobile-menu"
                aria-expanded="false"
                @click="toggleMobileMenu"
              >
                <span class="absolute -inset-0.5" id="mobile-menu-button"></span>
                <span class="sr-only">Open main menu</span>
                <svg
                  v-if="!mobileMenuOpen"
                  class="block size-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  aria-hidden="true"
                  data-slot="icon"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                  />
                </svg>
                <!-- Icon when menu is open -->
                <svg
                  v-else
                  class="block size-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  aria-hidden="true"
                  data-slot="icon"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6 18 18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
              <div class="flex shrink-0 items-center">
                <img class="size-8 rounded-full w-auto" src="https://assets.rebelmouse.io/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZSI6Imh0dHBzOi8vYXNzZXRzLnJibC5tcy80MTQwOTkyL29yaWdpbi5qcGciLCJleHBpcmVzX2F0IjoxNjQ2OTUzODEyfQ.apjxMWMTOb6ecQaPERNuuUJ5NBOwnidI0uiPuhtKXTw/img.jpg" alt="Logo" />
              </div>
              <div class="hidden sm:ml-6 sm:block">
                <div class="flex space-x-4">
                    <!-- Using nuxt-link -->
                <nuxt-link
                    to="/"
                    class="rounded-md  px-3 py-2 text-sm font-medium text-white"
                    :class="{ 'bg-gray-900': $route.path === '/' }"
                    aria-current="page">Dashboard</nuxt-link>
                
                <nuxt-link
                  to="/newpost"
                  class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                  :class="{ 'bg-gray-900': $route.path === '/newpost',
                  'hidden': user.status !== 'Administrator' 
                  }"
                >Create Post</nuxt-link>
                
                
              </div>
            </div>
          </div>
          <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0" v-if="isLoggedIn">
            <a
              type="button"
              class="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 "
              href="/profile"
            >
              {{ user.username }}
            </a>

            <!-- Profile dropdown -->
            <div class="relative ml-3">
              <div>
                <button
                  type="button"
                  
                  class="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                  id="user-menu-button"
                  aria-expanded="false"
                  aria-haspopup="true"
                  @click="toggleProfileDropdown"
                >
                  <span class="absolute -inset-1.5" id = "profile-btn"></span>
                  <span class="sr-only">Open user menu</span>
                    <!-- Image as placeholder -->
                  <img
                    class="size-8 rounded-full object-cover"
                    :src="user.avatar"
                    alt=""
                  />
                </button>
              </div>

              <!-- Dropdown menu, show/hide based on menu state. -->
                <div
                    v-if="profileDropdownOpen"
                    id = "profilemenu"
                    class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black/5 focus:outline-none"
                    role="menu"
                    aria-orientation="vertical"
                    aria-labelledby="user-menu-button"
                    tabindex="-1"
                >
                  <!-- Active: "bg-gray-100 outline-none", Not Active: "" -->
                  <a
                    href="/profile"
                    class="block px-4 py-2 text-sm text-gray-700"
                    role="menuitem"
                    tabindex="-1"
                    id="user-menu-item-0"
                    >Your Profile</a
                  ><a
                    href="/settings"
                    class="block px-4 py-2 text-sm text-gray-700"
                    role="menuitem"
                    tabindex="-1"
                    id="user-menu-item-1"
                    >Settings</a
                  >
                  <a
                    href=""
                    class="block px-4 py-2 text-sm text-gray-700"
                    role="menuitem"
                    tabindex="-1"
                    id="user-menu-item-2"
                    @click="logOut()"
                    >Sign out</a
                  >
                </div>
            </div>
          </div>
          <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0 text-gray-300" v-if="!isLoggedIn">
             <nuxt-link
                to="/signin"
                :class="{ 'bg-gray-900': $route.path === '/signin' }"
                class="block rounded-md px-3 py-2 text-base font-medium text-gray-200 hover:bg-gray-700 hover:text-white">
                
            Sign in
            </nuxt-link>
            <nuxt-link
                to="/signup"
                :class="{ 'bg-gray-900': $route.path === '/signup' }"
                class="block rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white">
            Sign up
            </nuxt-link>
          </div>

        </div>
      </div>

      <div class="sm:hidden" id="mobile-menu" v-if="mobileMenuOpen">
        <div class="space-y-1 px-2 pb-3 pt-2">
        <nuxt-link
            to="/"
            class="block rounded-md  px-3 py-2 text-base font-medium text-white"
            :class="{ 
              'bg-gray-900': $route.path === '/' }"
            aria-current="page">
            Dashboard
        </nuxt-link>
        <nuxt-link
            to="/newpost"
            :class="{ 
                  'bg-gray-900': $route.path === '/newpost',
                  'hidden': user.status !== 'Administrator' 
            }"
            class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white">

            Create Post
        </nuxt-link>
        
        
        </div>
      </div>
    </nav>
  </header>
</template>
