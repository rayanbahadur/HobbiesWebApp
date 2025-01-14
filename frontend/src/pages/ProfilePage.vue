<template>
    <div>
      <h1>Profile Page</h1>
      <div v-if="user">
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Date of Birth:</strong> {{ user.date_of_birth }}</p>
        <p><strong>Hobbies:</strong></p>
        <ul>
          <li v-for="hobby in user.hobbies" :key="hobby.id">{{ hobby.name }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted } from 'vue';
  import { useUserStoreProfile } from '../store/userStore';
  
  export default defineComponent({
    setup() {
      const userStore = useUserStoreProfile();
  
      onMounted(() => {
        userStore.fetchProfile();
      });
  
      return {
        user: userStore.user,
      };
    },
  });
  </script>
  
  <style scoped>
  </style>