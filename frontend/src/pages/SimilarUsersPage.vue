<template>
  <div>
    <h1>Users with Similar Hobbies</h1>
    <div>
      <label>Age Min:</label>
      <input type="number" v-model="ageMin" />
      <label>Age Max:</label>
      <input type="number" v-model="ageMax" />
      <button @click="applyFilters">Filter</button>
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
import { defineComponent, ref, onMounted, watch } from 'vue';
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
    const users = ref<User[]>([]); // Local reactive variable for users
    const ageMin = ref<number | null>(null);
    const ageMax = ref<number | null>(null);
    const page = ref<number>(1); // Local reactive variable for page

    const applyFilters = () => {
      userStore.setAgeFilter(ageMin.value, ageMax.value); // Apply filters in the store
    };

    const prevPage = () => {
      if (page.value > 1) {
        userStore.setPage(page.value - 1);
      }
    };

    const nextPage = () => {
      if (page.value < userStore.numPages) {
        userStore.setPage(page.value + 1);
      }
    };

    // Sync the reactive store state with the local `users` and `page` refs
    watch(
      () => userStore.users,
      (newUsers: User[]) => {
        users.value = newUsers; // Update reactive `users`
        console.log('Users updated in component:', newUsers);
      },
      { immediate: true } // Trigger immediately on mount
    );

    watch(
      () => userStore.page,
      (newPage: number) => {
        page.value = newPage; // Update reactive `page`
        console.log('Page updated in component:', newPage);
      },
      { immediate: true } // Trigger immediately on mount
    );

    onMounted(() => {
      userStore.fetchUsers(); // Fetch users on page load
    });

    return {
      users,
      page,
      numPages: userStore.numPages,
      ageMin,
      ageMax,
      applyFilters,
      prevPage,
      nextPage,
    };
  },
});
</script>