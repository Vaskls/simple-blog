
<template>
  <div class="container mx-auto p-4">
    <PostHeader :author="post.author" :createdAt="post.createdAt" :title="post.title" />
    <PostContent :content="post.content" />
    <PostReaction :post_id="post.id" :likes="post.likes" :dislikes="post.dislikes" :current_reaction="current_reaction"/>
    <CommentSection :post_id="post.id" :comments="post.comments" />
  </div>
</template>

<script setup>
const { $listen } = useNuxtApp();

import { ref, onMounted } from 'vue';
import { useRouter } from '#app';
import apiService from '~/api/api.js';
import PostHeader from '../elements/PostHeader.vue';
import PostContent from '../elements/PostContent.vue';
import CommentSection from '../elements/CommentSection.vue';
import PostReaction from "../elements/PostReaction.vue"
import { comment } from 'postcss';

const router = useRouter();
const current_reaction = ref(undefined)
const post = ref({
  id: 0,
  author: {
      name: "Author",
      avatar: "",
  },
  title: "Post title",
  content: "Post content",
  createdAt: "2024-07-21T10:00:00Z",
  likes: 0,
  dislikes: 0,
  comments: [
      {
        author: {
            name: "Comment username",
            avatar: "avatar"
        },
        content: "Comment content",
        createdAt: "2024-07-21T11:00:00Z"
      },
  ],
  
});




$listen('comment:add', (comment) => {
  post.value.comments.push(comment);
  console.log(post.value.comments)
});
$listen('reaction:add', (reaction) => {
  if (reaction === current_reaction.value) {
    if (current_reaction.value === false) { post.value.dislikes -- }
    if (current_reaction.value === true) { post.value.likes -- }
    current_reaction.value = undefined; // Undo reaction
    console.log(current_reaction.value)
    console.log("UNDO ACTION")
    return;
  }

  if (reaction === true) {
    if (current_reaction.value === false) { post.value.dislikes -- }
      current_reaction.value = reaction;
      post.value.likes ++
  }
  if (reaction === false) {
      if (current_reaction.value === true) { post.value.likes -- }
      current_reaction.value = reaction;
      post.value.dislikes ++
  }
});


onMounted(async () => {

  const post_id = router?.currentRoute?.value?.path.replace("/post/", "")
  let post_data = {}
  try {
    post_data = await apiService.get(`/post/${post_id}`) 
  } catch {
    window.location.href = "/notfound"
  }
  const post_reactions = await apiService.get(`/reaction/${post_id}`)
  try {
    const response = await apiService.get(`/reaction/${post_id}/my`)
    current_reaction.value = response.value
  } catch (e) {
    current_reaction.value = undefined
  }

  if (!post_data.post) {
    window.location.href = "/notfound"
  }
  let formatted_comments = []
  for (let comment of post_data.comments) {
    formatted_comments.push(
      {
        author: {
          username: comment.by_user.username,
          avatar: comment.by_user.avatar
        },
        contents: comment.contents,
        created: comment.created
      }
    )
  }
  post.value = {
    id: post_data.post.id,
    author: {
      username: post_data.post.by_user.username,
      avatar: post_data.post.by_user.avatar
    },
    title: post_data.post.header,
    content: post_data.post.contents,
    createdAt: post_data.post.created,
    likes: post_reactions.likes,
    dislikes: post_reactions.dislikes,
    comments: formatted_comments
  }
})
</script>