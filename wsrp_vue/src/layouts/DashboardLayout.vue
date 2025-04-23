<script setup>
import { ref, onMounted } from "vue";
import { jwtDecode } from "jwt-decode";
import NavBar from "../components/NavBar.vue";
import AdminDashboard from "../components/AdminDashboard.vue";
import CustomerDashboard from "../components/CustomerDashboard.vue";

const userProfile = ref(null);
const decodedToken = jwtDecode(localStorage.getItem("access_token"));
const user_name = decodedToken.sub;

const options = {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers":
      "Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers",
    Authorization: "Bearer " + localStorage.getItem("access_token"),
  },
};

const fetchUserProfile = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/users?user_name='" + user_name + "'",
      options
    );
    if (response.ok) {
      userProfile.value = await response.json();
    }
  } catch (error) {
    console.error("Error fetching profile:", error);
  }
};

onMounted(async () => {
  await fetchUserProfile();
});
</script>

<template>
  <div class="dashboard-layout">
    <NavBar />
    <div v-if="userProfile">
      <div v-if="userProfile.user.user_type === 'EMPLOYEE'">
        <AdminDashboard :userProfile="userProfile" />
      </div>
      <div v-else>
        <CustomerDashboard :userProfile="userProfile" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-layout {
  width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}
</style>
