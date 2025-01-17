<template>
    <div class="container">
      <h2>Friends Page</h2>
  
      <!-- Friends List -->
      <section>
        <h3>Friends</h3>
        <ul v-if="friends.length">
          <li v-for="friend in friends" :key="friend.id">
            {{ friend.name }}
          </li>
        </ul>
        <p v-else>No friends found.</p>
      </section>
  
      <!-- Friend Requests -->
      <section>
        <h3>Friend Requests</h3>
        <ul v-if="friendRequests.length">
          <li v-for="request in friendRequests" :key="request.id">
            {{ request.from_user.name || 'Unknown' }} sent a request <!-- Use `from_user.name` -->
            <button @click="acceptRequest(request.id)">Accept</button>
            <button @click="rejectRequest(request.id)">Reject</button>
          </li>
        </ul>
        <p v-else>No friend requests found.</p>
      </section>

  
      <!-- Search for Friends -->
      <section>
        <h3>Search for Friends</h3>
        <input
          v-model="searchQuery"
          placeholder="Search by username"
          @keyup.enter="searchFriends"
        />
        <button @click="searchFriends">Search</button>
        <ul v-if="searchResults.length">
          <li v-for="user in searchResults" :key="user.id">
            {{ user.username }}
            <button @click="sendFriendRequest(user.id)">Send Friend Request</button>
          </li>
        </ul>
        <p v-else>No results found.</p>
      </section>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  
  export default defineComponent({
    setup() {
      // Data
      const friends = ref([]);
      const friendRequests = ref([]);
      const searchQuery = ref("");
      const searchResults = ref([]);
  
      // Fetch friends
      const fetchFriends = async () => {
        try {
          const response = await fetch("/api/friends/");
          if (!response.ok) throw new Error("Failed to fetch friends");
          friends.value = await response.json();
        } catch (error) {
          console.error(error.message);
        }
      };
  
      // Fetch friend requests
      const fetchFriendRequests = async () => {
        try {
          const response = await fetch("/api/friend-requests/");
          if (!response.ok) throw new Error("Failed to fetch friend requests");
          const data = await response.json();
          console.log("Friend Requests:", data); // Debug log
          friendRequests.value = data;
        } catch (error) {
          console.error(error.message);
        }
      };
  
      // Search for friends
      const searchFriends = async () => {
        try {
          const response = await fetch(`/api/search/?q=${encodeURIComponent(searchQuery.value)}`);
          if (!response.ok) throw new Error("Failed to search users");
          searchResults.value = await response.json();
        } catch (error) {
          console.error(error.message);
        }
      };
      const getCSRFToken = () => {
        const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
        return csrfToken ? csrfToken.split('=')[1] : '';
      };
    
      // Send friend request
      const sendFriendRequest = async (userId: number) => {
        try {
          const csrfToken = getCSRFToken();
          const response = await fetch("/api/friend-requests/send/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ to_user_id: userId }), // Correct payload
          });

          if (!response.ok) {
            const errorText = await response.text();
            try {
              const errorJson = JSON.parse(errorText);
              throw new Error(errorJson.error || "Failed to send friend request");
            } catch {
              throw new Error("Unexpected error occurred: " + errorText);
            }
          }

          alert("Friend request sent!");
        } catch (error) {
          console.error(error.erroe);
          alert(error.error);
        }
      };

  
      // Accept friend request
      const acceptRequest = async (requestId: number) => {
        try {
          const csrfToken = getCSRFToken();
          const response = await fetch("/api/friend-requests/accept/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken, // Include CSRF token in the headers
            },
            body: JSON.stringify({ request_id: requestId }), // Send request_id in the body
          });

          if (!response.ok) throw new Error("Failed to accept friend request");

          fetchFriendRequests(); // Refresh friend requests
          fetchFriends(); // Refresh friends list
        } catch (error) {
          console.error(error.error);
        }
      };

      // Reject friend request
      const rejectRequest = async (requestId: number) => {
        try {
          const csrfToken = getCSRFToken();
          const response = await fetch("/api/friend-requests/reject/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken, // Include CSRF token in the headers
            },
            body: JSON.stringify({ request_id: requestId }), // Send request_id in the body
          });

          if (!response.ok) throw new Error("Failed to reject friend request");

          fetchFriendRequests(); // Refresh friend requests
        } catch (error) {
          console.error(error.error);
        }
      };
      // Fetch initial data
      fetchFriends();
      fetchFriendRequests();
  
      return {
        friends,
        friendRequests,
        searchQuery,
        searchResults,
        fetchFriends,
        fetchFriendRequests,
        searchFriends,
        sendFriendRequest,
        acceptRequest,
        rejectRequest,
      };
    },
  });
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: 0 auto;
    padding: 1rem;
  }
  
  section {
    margin-bottom: 2rem;
  }
  
  input {
    margin-right: 1rem;
  }
  </style>
  