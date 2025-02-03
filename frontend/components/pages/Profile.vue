<script setup> 

const props = defineProps({
    user: {
        type: Object,
        required: true
    }
})

function formatDate() {
    const dateobject = new Date(props.user.joined)
    return dateobject.toLocaleDateString('en-GB', {
    day : 'numeric',
    month : 'short',
    year : 'numeric',
    hour : 'numeric',
    minute : 'numeric'
}).split(' ').join(' ');
}
const dateFormated = ref(formatDate())

onMounted(() => {
    if (!props.user.username) {
        window.location.href = "/"
    }
})

</script>




<template>
    
    <div class="mt-10">
        <div class="flex mx-3 flex-col my-1 items-center justify-center sm:mx-0">
                <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full p-8 transition-all">
                    <div class="flex flex-col md:flex-row">
                        <div class="md:w-1/3 text-center mb-8 md:mb-0">
                            <img :src="user.avatar" alt="Profile Picture" class="size-36 rounded-full object-cover mx-auto mb-4 border-4 border-indigo-800 dark:border-blue-900 hover:scale-105">

                            <h1 class="text-2xl font-bold text-indigo-800 dark:text-white mb-2"> {{ user.username }} </h1>
                            <p class="text-gray-600 dark:text-gray-300">{{ user.status }}</p>
                            
                        </div>
                        <div class="md:w-2/3 md:pl-8">
                            <h2 class="text-xl font-semibold text-indigo-800 dark:text-white mb-4">About Me</h2>
                            <p class="text-gray-700 dark:text-gray-300 mb-6">
                                Signed up: {{ dateFormated }}
                            </p>
                            <p class="text-gray-700 dark:text-gray-300 mb-6">
                                Total comments: {{ user.total_posts }}
                            </p>
                            <p class="text-gray-700 dark:text-gray-300 mb-6">
                                Total reactions: {{ user.total_reactions }}
                            </p>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>