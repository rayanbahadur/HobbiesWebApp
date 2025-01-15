import { defineStore } from 'pinia';

interface Hobby {
  id: number;
  name: string;
}

interface User {
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: Hobby[];
}


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

export const useUserStoreProfile = defineStore('userStoreProfile', {
  state: () => ({
    user: null as User | null,
  }),
  actions: {
    async fetchProfile() {
      const response = await fetch('/api/profile/');
      const data: User = await response.json();
      this.user = data;
    },
    async updateProfile(updatedUser: User) {
      const response = await fetch('/api/profile/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedUser),
      });
      if (response.ok) {
        this.user = await response.json();
      } else {
        const errorData = await response.json();
        throw new Error(errorData.errors);
      }
    },
  },
});