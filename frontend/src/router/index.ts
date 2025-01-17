// Example of how to use Vue Router

import { createRouter, createWebHistory } from "vue-router";
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
      path: "/",
      name: "Similar Users",
      component: SimilarUsersPage,
    },
    {
      path: "/friends/",
      name: "Friends Page",
      component: FriendsPage, // Navigate to FriendsPage component
    },
    { 
      path: "/profile/", 
      name: "Profile Page",
      component: ProfilePage,
      beforeEnter: () => {
        const userStore = useUserStoreProfile();
        return userStore.fetchProfile(); // Ensure profile is fetched before entering the route
      },
    },
  ],
});

// Global navigation guard
router.beforeEach((to, from, next) => {
  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1]; // Extract the token value
  
  const matchedRoute = router.getRoutes().some(route => route.path === to.path);
  
  if (!csrfToken && to.path !== "/login") {
    console.log('No CSRF token found, redirecting to login page.');
    window.location.href = '/login';
  } else if (!matchedRoute) {
    console.log('No route matched, redirecting to login page.');
    window.location.href = '/login';
  } else {
    next();
  }
});

export default router;
