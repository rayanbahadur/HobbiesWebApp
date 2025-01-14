<template>
  <main class="container pt-4">
    <nav class="navbar navbar-inverse">
      <ul class="nav navbar-nav" style="flex-direction: row; gap: 2em">
        <li class="nav-item">
          <router-link class="nav-link" :to="{ name: 'Main Page' }">Main Page</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{ name: 'Profile Page' }">Profile Page</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{ name: 'Similar Users' }">Similar Users</router-link>
        </li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li class="nav-item">
          <LogoutButton />
        </li>
      </ul>
    </nav>
    <router-view />
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import LogoutButton from "./components/LogoutButton.vue";

export default defineComponent({
  components: { RouterView, LogoutButton },
});
</script>

<style scoped></style>