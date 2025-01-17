<template>
  <div>
    <h1 class="mb-4">Profile Page</h1>
    <div v-if="user">
      <form @submit.prevent="saveProfile">
        <div class="form-group mb-3">
          <label for="name" class="form-label custom-label">Name:</label>
          <input type="text" id="name" class="form-control" v-model="name" />
        </div>
        <div class="form-group mb-3">
          <label for="email" class="form-label custom-label">Email:</label>
          <input type="email" id="email" class="form-control" v-model="email" />
        </div>
        <div class="form-group mb-3">
          <label for="date_of_birth" class="form-label custom-label"
            >Date of Birth:</label
          >
          <input
            type="date"
            id="date_of_birth"
            class="form-control"
            v-model="date_of_birth"
          />
        </div>
        <div class="form-group mb-3">
          <label for="newPassword1" class="form-label custom-label"
            >New Password:</label
          >
          <input
            type="password"
            id="newPassword1"
            class="form-control"
            v-model="newPassword1"
            autocomplete="new-password"
          />
        </div>
        <div class="form-group mb-3">
          <label for="newPassword2" class="form-label custom-label"
            >Confirm New Password:</label
          >
          <input
            type="password"
            id="newPassword2"
            class="form-control"
            v-model="newPassword2"
            autocomplete="new-password"
          />
        </div>
        <div class="form-group mb-3">
          <label class="form-label custom-label">Hobbies:</label>
          <div v-for="hobby in allHobbies" :key="hobby.id" class="form-check">
            <input
              type="checkbox"
              :value="hobby.id"
              class="form-check-input"
              v-model="selectedHobbies"
            />
            <label class="form-check-label">{{ hobby.name }}</label>
          </div>
        </div>
        <div class="form-group mb-3">
          <label for="newHobby" class="form-label custom-label"
            >Add New Hobby:</label
          >
          <input
            type="text"
            id="newHobby"
            class="form-control"
            v-model="newHobby"
            placeholder="Add New Hobby (Optional)"
          />
        </div>
        <button type="submit" class="btn btn-success mb-3">Save</button>
      </form>
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useUserStoreProfile } from "../store/userStore";

interface Hobby {
  id: number;
  name: string;
}

export default defineComponent({
  setup() {
    const userStore = useUserStoreProfile();
    const allHobbies = ref<Hobby[]>([]);
    const selectedHobbies = ref<number[]>([]);
    const name = ref<string>("");
    const email = ref<string>("");
    const date_of_birth = ref<string>("");
    const newPassword1 = ref<string>("");
    const newPassword2 = ref<string>("");
    const newHobby = ref<string>("");
    const errorMessage = ref<string>("");

    onMounted(async () => {
      await userStore.fetchProfile();
      const response = await fetch("/api/hobbies/");
      if (response.ok) {
        allHobbies.value = await response.json();
        selectedHobbies.value =
          userStore.user?.hobbies.map((hobby) => hobby.id) || [];
      } else {
        console.error("Failed to fetch hobbies");
      }
      if (userStore.user) {
        name.value = userStore.user.name;
        email.value = userStore.user.email;
        date_of_birth.value = userStore.user.date_of_birth;
      }
    });

    const getCsrfToken = () => {
      const csrfToken = document.cookie
        .split(";")
        .find((cookie) => cookie.trim().startsWith("csrftoken="));
      return csrfToken ? csrfToken.split("=")[1] : "";
    };

    const validateEmail = (email: string): boolean => {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    };

    const validateDateOfBirth = (dob: string): boolean => {
      const selectedDate = new Date(dob);
      const currentDate = new Date();
      return selectedDate <= currentDate;
    };

    const saveProfile = async () => {
      if (!validateEmail(email.value)) {
        errorMessage.value = "Invalid email format";
        return;
      }

      if (!validateDateOfBirth(date_of_birth.value)) {
        errorMessage.value = "Date of birth cannot be in the future";
        return;
      }

      if (userStore.user) {
        const formData = new FormData();
        formData.append("name", name.value);
        formData.append("email", email.value);
        formData.append("date_of_birth", date_of_birth.value);
        if (newPassword1.value) {
          formData.append("new_password1", newPassword1.value);
          formData.append("new_password2", newPassword2.value);
        }
        selectedHobbies.value.forEach((hobbyId) =>
          formData.append("hobbies", hobbyId.toString())
        );

        if (newHobby.value) {
          formData.append("new_hobby", newHobby.value);
        }

        try {
          const response = await fetch("/api/profile/", {
            method: "POST",
            headers: {
              "X-CSRFToken": getCsrfToken(),
            },
            body: formData,
          });
          if (response.ok) {
            alert("Profile updated successfully");
            window.location.reload(); // Refresh the page after alert
          } else {
            const errorData = await response.json();
            handleErrors(errorData.errors);
          }
        } catch (error) {
          handleErrors((error as Error).message);
        }
      }
    };

    const handleErrors = (errors: any) => {
      if (typeof errors === "string") {
        errorMessage.value = errors;
      } else if (errors.__all__) {
        errorMessage.value = errors.__all__.join(", ");
      } else {
        errorMessage.value = Object.values(errors).flat().join(", ");
      }
    };

    return {
      user: userStore.user,
      name,
      email,
      date_of_birth,
      newPassword1,
      newPassword2,
      newHobby,
      allHobbies,
      selectedHobbies,
      saveProfile,
      errorMessage,
    };
  },
});
</script>

<style scoped>
.custom-label {
  font-size: 1.25rem;
  font-weight: bold;
}
</style>
