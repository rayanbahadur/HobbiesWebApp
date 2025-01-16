// Example of how to use Vue Router

import { createRouter, createWebHistory } from "vue-router";
import MainPage from "../pages/MainPage.vue";
import ProfilePage from "../pages/ProfilePage.vue";
import SimilarUsersPage from "../pages/SimilarUsersPage.vue";
import FriendsPage from "../pages/Friends.vue";

let base =
  import.meta.env.MODE == "development" ? import.meta.env.BASE_URL : "";

// Define routes
const router = createRouter({
  history: createWebHistory(base),
  routes: [
    { path: "/", name: "Main Page", component: MainPage },
    {
      path: "/profile/",
      name: "Profile Page",
      component: ProfilePage,
    },
    {
      path: "/similar-users/",
      name: "Similar Users",
      component: SimilarUsersPage,
    },
    {
      path: "/friends/",
      name: "Friends Page",
      component: FriendsPage, // Navigate to FriendsPage component
    },
  ],
});

// Global navigation guard
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
