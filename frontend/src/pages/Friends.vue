<template>
    <h1>Friends Page</h1>
    <div class="container">
  
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

  interface Friend {
    id: number;
    name: string;
  }

  interface FriendRequest {
    id: number;
    from_user: {
      id: number;
      name: string;
    };
  }

  interface SearchResult {
    id: number;
    username: string;
  }
  
  export default defineComponent({
    setup() {
      // Data
      const friends = ref<Friend[]>([]);
      const friendRequests = ref<FriendRequest[]>([]);
      const searchQuery = ref<string>("");
      const searchResults = ref<SearchResult[]>([]);
  
      // Fetch friends
      const fetchFriends = async () => {
        try {
          const response = await fetch("/api/friends/");
          if (!response.ok) throw new Error("Failed to fetch friends");
          friends.value = await response.json();
        } catch (error) {
          if (error instanceof Error) {
            console.error(error.message);
          } else {
            console.error(String(error));
          }
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
          if (error instanceof Error) {
            console.error(error.message);
          } else {
            console.error(String(error));
          }
        }
      };
  
      // Search for friends
      const searchFriends = async () => {
        try {
          const response = await fetch(`/api/search/?q=${encodeURIComponent(searchQuery.value)}`);
          if (!response.ok) throw new Error("Failed to search users");
          searchResults.value = await response.json();
        } catch (error) {
          if (error instanceof Error) {
            console.error(error.message);
          } else {
            console.error(String(error));
          }
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
              if (errorJson.error === "You are already friends") {
                alert("You are already friends with this user.");
              } else {
                throw new Error(errorJson.error || "Failed to send friend request");
              }
            } catch {
              throw new Error("Unexpected error occurred: " + errorText);
            }
          } else {
            alert("Friend request sent!");
          }
        } catch (error) {
          if (error instanceof Error) {
            console.error(error.message);
            alert(error.message);
          } else {
            console.error(String(error));
            alert("An unexpected error occurred.");
          }          
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

          if (!response.ok) {
            const errorText = await response.text();
            try {
              const errorJson = JSON.parse(errorText);
              throw new Error(errorJson.error || "Failed to accept friend request");
            } catch {
              throw new Error("Unexpected error occurred: " + errorText);
            }
          }

          fetchFriendRequests(); // Refresh friend requests
          fetchFriends(); // Refresh friends list
        } catch (error) {
          if (error instanceof Error) {
            console.error(error.message);
            alert(error.message);
          } else {
            console.error(String(error));
            alert("An unexpected error occurred.");
          }          
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

          if (!response.ok) {
            const errorText = await response.text();
            try {
              const errorJson = JSON.parse(errorText);
              throw new Error(errorJson.error || "Failed to reject friend request");
            } catch {
              throw new Error("Unexpected error occurred: " + errorText);
            }
          }

          fetchFriendRequests(); // Refresh friend requests
        } catch (error) {
          if (error instanceof Error) {
            console.error(error.message);
            alert(error.message);
          } else {
            console.error(String(error));
            alert("An unexpected error occurred.");
          }          
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