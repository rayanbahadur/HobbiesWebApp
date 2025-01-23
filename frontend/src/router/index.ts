// Example of how to use Vue Router

import { createRouter, createWebHistory } from "vue-router";
import ProfilePage from "../pages/ProfilePage.vue";
import SimilarUsersPage from "../pages/SimilarUsersPage.vue";
import FriendsPage from "../pages/Friends.vue";
import { useUserStore, useUserStoreProfile } from '../store/userStore';


let base =
  import.meta.env.MODE == "development" ? import.meta.env.BASE_URL : "";

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
  history: createWebHistory(base),
  routes: [
    {
      path: "/",
      name: "Similar Users",
      component: SimilarUsersPage,
      beforeEnter: () => {
        const userStore = useUserStore();
        return userStore.fetchUsers(); // Ensure users are fetched before entering the route
      },
    },
    {
      path: "/friends-page/",
      name: "Friends Page",
      component: FriendsPage, // Navigate to FriendsPage component
    },
    { 
      path: "/profile-page/", 
      name: "Profile Page",
      component: ProfilePage,
      beforeEnter: () => {
        console.log('Fetching profile data before entering the route');
        const userStore = useUserStoreProfile();
        return userStore.fetchProfile(); // Ensure profile is fetched before entering the route
      },
    },
  ],
});

router.beforeEach((to, _from, next) => {
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
