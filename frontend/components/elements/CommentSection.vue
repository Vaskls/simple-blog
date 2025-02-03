<template>
  <div class="mb-8">
    <h2 class="text-lg font-semibold mb-2">Comments</h2>
    <div class="mb-4">
      <textarea
        v-model="newComment"
        class="w-full p-2 border rounded"
        rows="3"
        placeholder="Add a comment..."
      ></textarea>
      <button @click="addComment" class="bg-blue-500 text-white py-2 px-4 rounded mt-2">
        Comment
      </button>
    </div>
     <div v-if="comments.length > 0">
         <CommentItem
             v-for="comment in comments"
             :key="comment.created"
             :comment="comment"
         />
     </div>
    <div v-else>
        There are currently no comments
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CommentItem from './CommentItem.vue';
import apiService from '~/api/api';
const { $event } = useNuxtApp()

const props = defineProps({
  comments: {
    type: Array,
    required: true,
  },
  post_id: {
    type: Number,
    required: true
  },
  user: {
    type: Object,
    required: false
  }
});

const newComment = ref('');



async function addComment() {
  if(newComment.value.length === 0){
      return
  }
  
  try {
    const result = await apiService.post("/post/", {
        header: null,
        contents: newComment.value,
        iscomment: true,
        response_to_id: props.post_id
    })
    
    const comment_obj = {
      author: {
        username: localStorage.getItem('username'),
        avatar: localStorage.getItem('avatar')
      },
      contents: result.contents,
      created: result.created,
    }
    $event('comment:add', comment_obj)
    newComment.value = ""
  } catch {
    return alert("You have to be authorised to perform this action")
  }

};


</script>