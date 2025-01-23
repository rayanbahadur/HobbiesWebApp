<template>
  <button class="btn btn-danger" id="logout" name="logout" @click="logout">Logout</button>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "LogoutButton",
  methods: {
    async logout() {
      try {
        const csrfToken = this.getCookie("csrftoken");
        const headers: HeadersInit = {
          "Content-Type": "application/json",
        };

        if (csrfToken) {
          headers["X-CSRFToken"] = csrfToken;
        }

        const response = await fetch("/logout/", {
          method: "POST",
          headers,
        });

        if (response.ok) {
          window.location.href = "/login/";
        } else {
          console.error("Logout failed");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    getCookie(name: string) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
  },
});
</script>

<style scoped>
/* Add any additional styles here */
</style>
