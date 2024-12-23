// Example of how to use Vue Router

import { createRouter, createWebHistory } from "vue-router";
import MainPage from "../pages/MainPage.vue";
import OtherPage from "../pages/OtherPage.vue";
import SimilarUsersPage from "../pages/SimilarUsersPage.vue";
import { useUserStore } from '../store/userStore';

let base =
  import.meta.env.MODE == "development" ? import.meta.env.BASE_URL : "";

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
  history: createWebHistory(base),
  routes: [
    { path: "/", name: "Main Page", component: MainPage },
    { path: "/other/", name: "Other Page", component: OtherPage },
    {
      path: "/similar-users/",
      name: "Similar Users",
      component: SimilarUsersPage,
      beforeEnter: () => {
        const userStore = useUserStore();
        return userStore.fetchUsers(); // Ensure users are fetched before entering the route
      },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));
  if (!csrfToken && to.path !== "/login") {
    window.location.href = "/login";
  } else {
    next();
  }
});
export default router;
