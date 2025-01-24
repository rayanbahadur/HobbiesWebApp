<template>
  <div>
    <h1 class="mb-4">Users with Similar Hobbies</h1>
    <div class="row g-2 mb-3">
      <div class="input-group col mb-3">
        <span for="ageMin" class="input-group-text" id="inputGroup-sizing-default">Min Age</span>
        <input type="number" id="ageMin" v-model="ageMin" class="form-control" />
      </div>
      <div class="input-group col mb-3">
        <span for="ageMax" class="input-group-text" id="inputGroup-sizing-default">Max Age</span>
        <input type="number" id="ageMax" v-model="ageMax" class="form-control" />
      </div>
      <div class="col mb-3">
        <button  type="submit" @click="applyFilters" class="btn btn-primary w-30">Filter</button>
      </div>
    </div>
    <ul class="list-group">
      <li v-for="user in users" :key="user.email" class="list-group-item d-flex justify-content-between align-items-center">
        {{ user.name }}
        <span class="badge bg-secondary rounded-pill">{{ user.common_hobbies }} {{user.common_hobbies > 1? "shared hobbies" : "shared hobby"}}</span>
      </li>
    </ul>
    <div v-if="users.length === 0" class="alert alert-warning mt-3" role="alert">
      No Results found. Adjust Filters and try again.
    </div>
    <div class="btn-group mt-3" role="group" aria-label="Pagination">
      <button class="btn btn-outline-secondary" @click="prevPage" :disabled="page <= 1">Previous</button>
      <button class="btn btn-outline-secondary" @click="nextPage" :disabled="page >= numPages">Next</button>
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