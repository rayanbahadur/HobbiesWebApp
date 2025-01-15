<template>
  <div>
    <h1>Profile Page</h1>
    <div v-if="user">
      <form @submit.prevent="saveProfile">
        <div>
          <label>Name:</label>
          <input type="text" v-model="user.name" />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" v-model="user.email" />
        </div>
        <div>
          <label>Date of Birth:</label>
          <input type="date" v-model="user.date_of_birth" />
        </div>
        <div>
          <label>New Password:</label>
          <input type="password" v-model="newPassword1" />
        </div>
        <div>
          <label>Confirm New Password:</label>
          <input type="password" v-model="newPassword2" />
        </div>
        <div>
          <label>Hobbies:</label>
          <div v-for="hobby in allHobbies" :key="hobby.id">
            <input
              type="checkbox"
              :value="hobby.id"
              v-model="selectedHobbies"
            />
            {{ hobby.name }}
          </div>
        </div>
        <button type="submit">Save</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useUserStoreProfile } from '../store/userStore';

interface Hobby {
  id: number;
  name: string;
}

export default defineComponent({
  setup() {
    const userStore = useUserStoreProfile();
    const allHobbies = ref<Hobby[]>([]);
    const selectedHobbies = ref<number[]>([]);
    const newPassword1 = ref<string>('');
    const newPassword2 = ref<string>('');

    onMounted(async () => {
      await userStore.fetchProfile();
      const response = await fetch('/api/hobbies/');
      if (response.ok) {
        allHobbies.value = await response.json();
        selectedHobbies.value = userStore.user?.hobbies.map(hobby => hobby.id) || [];
      } else {
        console.error('Failed to fetch hobbies');
      }
    });

    const getCsrfToken = () => {
      const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
      return csrfToken ? csrfToken.split('=')[1] : '';
    };

    const saveProfile = async () => {
      if (userStore.user) {
        const formData = new FormData();
        formData.append('name', userStore.user.name);
        formData.append('email', userStore.user.email);
        formData.append('date_of_birth', userStore.user.date_of_birth);
        if (newPassword1.value) {
          formData.append('new_password1', newPassword1.value);
          formData.append('new_password2', newPassword2.value);
        }
        selectedHobbies.value.forEach(hobbyId => formData.append('hobbies', hobbyId.toString()));

        try {
          const response = await fetch('/api/profile/', {
            method: 'POST',
            headers: {
              'X-CSRFToken': getCsrfToken(),
            },
            body: formData,
          });
          if (response.ok) {
            alert('Profile updated successfully');
            await userStore.fetchProfile(); // Fetch the updated profile
          } else {
            const errorData = await response.json();
            alert('Error updating profile: ' + JSON.stringify(errorData));
          }
        } catch (error) {
          alert('Error updating profile: ' + (error as Error).message);
        }
      }
    };

    return {
      user: userStore.user,
      allHobbies,
      selectedHobbies,
      newPassword1,
      newPassword2,
      saveProfile,
    };
  },
});
</script>

<style scoped>
/* Add your styles here */
</style>