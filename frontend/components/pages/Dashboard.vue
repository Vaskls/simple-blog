

<script setup>
import PostItem from '~/components/elements/PostItem.vue';
import apiService from '~/api/api';

const posts = await apiService.get("/post/posts")
console.log(posts)
</script>


<template>
  <div class="mt-5">
    <div class="flex mx-3 flex-col my-1 items-center justify-center sm:mx-0" 
        v-for="(post, index) in posts" :key="index">
          <PostItem
            :post=post
          />
    </div>
  </div>
      


</template>

