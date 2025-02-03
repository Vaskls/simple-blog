<template>
    
    <div class="relative flex flex-col rounded-lg border border-slate-200 bg-white shadow-sm max-w-[1000px] w-full" >
      <a :href="/post/ + post.id">
      
      <nav class="flex min-w-[240px] flex-col gap-1 p-1.5">
          <div
            role="button"
            class="text-slate-800 flex w-full items-center rounded-md p-3 transition-all hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100" 
          >
            <div>
              <div class="mr-4 grid place-items-center">
                <img
                  alt="candice"
                  :src=post.by_user.avatar
                  class="relative inline-block !rounded-full object-cover object-center h-8 w-8 lg:h-12 lg:w-12"
                />
              </div>
            </div>
            <div class="flex flex-col">
              <h6 class="text-slate-800 font-medium truncate max-w-xs lg:max-w-lg">
                {{ post.header }}
              </h6>
              <p class="text-slate-500 text-sm truncate max-w-xs lg:max-w-lg">
                {{ post.contents }}
              </p>
              <p class="text-gray-400 text-sm truncate max-w-xs lg:max-w-lg">
                <strong class="text-gray-800">By: </strong>{{ post.by_user.username }}
              </p>
            </div>
        </div>
      </nav>
      </a>
    </div>
</template>

<script setup>


const props = defineProps({
    post: {
      type: Object,
      required: true,

    }
});
</script>