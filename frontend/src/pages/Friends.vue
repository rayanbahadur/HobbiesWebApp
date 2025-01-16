<template>
    <div class="container">
      <h2>Friends Page</h2>
  
      <!-- Friends List -->
      <section>
        <h3>Friends</h3>
        <ul v-if="friends.length">
          <li v-for="friend in friends" :key="friend.id">
            {{ friend.username }} (Friends since: {{ friend.since }})
          </li>
        </ul>
        <p v-else>No friends found.</p>
      </section>
  
      <!-- Friend Requests -->
      <section>
        <h3>Friend Requests</h3>
        <ul v-if="friendRequests.length">
          <li v-for="request in friendRequests" :key="request.id">
            {{ request.from_user.username }} sent a request
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
          friendRequests.value = await response.json();
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
  
      // Send friend request
      const sendFriendRequest = async (userId) => {
        try {
          const response = await fetch("/api/friend-requests/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ to_user_id: userId }),
          });
          if (!response.ok) throw new Error("Failed to send friend request");
          alert("Friend request sent!");
        } catch (error) {
          console.error(error.message);
        }
      };
  
      // Accept friend request
      const acceptRequest = async (requestId) => {
        try {
          const response = await fetch("/api/friend-requests/accept/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ request_id: requestId }),
          });
          if (!response.ok) throw new Error("Failed to accept friend request");
          fetchFriendRequests(); // Refresh friend requests
          fetchFriends(); // Refresh friends list
        } catch (error) {
          console.error(error.message);
        }
      };
  
      // Reject friend request
      const rejectRequest = async (requestId) => {
        try {
          const response = await fetch("/api/friend-requests/reject/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ request_id: requestId }),
          });
          if (!response.ok) throw new Error("Failed to reject friend request");
          fetchFriendRequests(); // Refresh friend requests
        } catch (error) {
          console.error(error.message);
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
  