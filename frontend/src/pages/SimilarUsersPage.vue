<template>
  <div>
    <h1>Users with Similar Hobbies</h1>
    <div>
      <label>Age Min:</label>
      <input type="number" v-model="ageMin" @change="updateFilter" />
      <label>Age Max:</label>
      <input type="number" v-model="ageMax" @change="updateFilter" />
    </div>
    <ul>
      <li v-for="user in users" :key="user.email">
        {{ user.name }} ({{ user.common_hobbies }} common hobbies)
      </li>
    </ul>
    <div>
      <button @click="prevPage" :disabled="page <= 1">Previous</button>
      <button @click="nextPage" :disabled="page >= numPages">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useUserStore } from '../store/userStore';

interface User {
  name: string;
  email: string;
  date_of_birth: string;
  common_hobbies: number;
}

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const ageMin = ref<number | null>(null);
    const ageMax = ref<number | null>(null);

    const updateFilter = () => {
      userStore.setAgeFilter(ageMin.value, ageMax.value);
    };

    const prevPage = () => {
      if (userStore.page > 1) {
        userStore.setPage(userStore.page - 1);
      }
    };

    const nextPage = () => {
      if (userStore.page < userStore.numPages) {
        userStore.setPage(userStore.page + 1);
      }
    };

    // Add this to debug user data when the component is mounted
    onMounted(() => {
      userStore.fetchUsers().then(() => {
        console.log('Users:', userStore.users); // Debugging the users
      });
    });

    return {
      users: userStore.users as User[],
      page: userStore.page,
      numPages: userStore.numPages,
      ageMin,
      ageMax,
      updateFilter,
      prevPage,
      nextPage,
    };
  },
});
</script>