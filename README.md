# Hobbies Web App - README

## Team Members and Contributions

### Rayan
- **Assigned Task:** User authentication and account creation (signup, login, logout) using Django's authentication framework, custom User model, and Django templates.
- **Contribution:** Implemented account creation and login/logout functionality, designed the custom User model with additional fields (name, email, date of birth, hobbies), and integrated server-side rendering for templates.

### Ahmad
- **Assigned Task:** Develop the "similar users" feature with hobby matching, filtering by age, and pagination.
- **Contribution:** Created a page displaying users with the most similar hobbies in descending order, implemented AJAX-based filtering and pagination to fetch only necessary user data dynamically.

### Abdullah
- **Assigned Task:** User profile management, allowing users to edit profile data and hobbies.
- **Contribution:** Developed the profile page, enabling users to update their name, email, date of birth, hobbies, and password.

### Rahul
- **Assigned Task:** Implement a friend request system with AJAX functionality.
- **Contribution:** Designed and implemented the friend request feature, including sending requests, approving requests, and establishing friendships between users.

### Rahul and Abdullah
- **Assigned Task:** Automated testing of core features.
- **Contribution:** Developed Selenium-based end-to-end (E2E) tests covering account creation, login, profile editing, user page filtering, sending and accepting friend requests.

---

## Deployed Application
- **URL:** https://group-25-web-apps-ec22431.apps.a.comp-teach.qmul.ac.uk/

---

## Admin User Credentials
- **Username:** admin@hobbies.com
- **Password:** #Pass123#

---

## Test User Credentials
Here are the credentials for 5 test users:

1. **Username:** alice.smith@hobbies.com  
   **Password:** #Pass123#

2. **Username:** bob.johnson@hobbies.com  
   **Password:** #Pass123#

3. **Username:** carol.davis@hobbies.com  
   **Password:** #Pass123#

4. **Username:** david.martinez@hobbies.com  
   **Password:** #Pass123#

5. **Username:** emily.brown@hobbies.com  
   **Password:** #Pass123#

---

## Features Summary

### Rayan
- Account creation and authentication using Django's custom User model and templates.
- Hobbies are database-driven, allowing users to add new hobbies dynamically.

### Ahmad
- Similar users feature displaying users with the most shared hobbies.
- AJAX-based filtering by age and pagination for efficient data fetching.

### Abdullah
- Profile management: Users can edit their details and hobbies on a dedicated profile page.
- Automated E2E testing using Selenium for core features.

### Rahul
- Friend request system with AJAX-based request sending and approval.
- Automated E2E testing using Selenium for core features.

### Automated Testing
The following features are covered by automated Selenium tests:
1. Account creation/signup.
2. Login functionality.
3. Editing user profile data (name, email, DOB, hobbies, password).
4. Viewing and filtering users by age.
5. Sending a friend request.
6. Logging in as another user and accepting the friend request.

