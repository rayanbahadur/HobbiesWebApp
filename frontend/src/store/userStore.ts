import { defineStore } from 'pinia';

export const useUserStore = defineStore('userStore', {
  state: () => ({
    users: [],
    page: 1,
    numPages: 1,
    ageMin: null as number | null,
    ageMax: null as number | null,
  }),
  actions: {
    async fetchUsers() {
      const params = new URLSearchParams({
        age_min: this.ageMin?.toString() || '',
        age_max: this.ageMax?.toString() || '',
        page: this.page.toString(),
      });

      console.log('Fetching users with params:', params.toString()); // Debugging log
      const response = await fetch(`/api/similar/?${params.toString()}`);
      const data = await response.json();
      console.log('Fetched users:', data); // Debugging log
      this.users = data.users;
      this.numPages = data.num_pages;
    },
    setAgeFilter(ageMin: number | null, ageMax: number | null) {
      this.ageMin = ageMin;
      this.ageMax = ageMax;
      this.page = 1;
      this.fetchUsers();
    },
    setPage(page: number) {
      this.page = page;
      this.fetchUsers();
    },
  },
});