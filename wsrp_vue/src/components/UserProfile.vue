<script setup>
import { ref, onMounted } from "vue";
import { jwtDecode } from "jwt-decode";
import NavBar from "./NavBar.vue";

// parse the user_name from the current jwt token
const decodedToken = jwtDecode(localStorage.getItem("access_token"));
const user_name = decodedToken.sub;
const userProfile = ref(null);

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
      `${import.meta.env.VITE_API_URL}/api/users?user_name=${user_name}`,
      options
    );
    if (response.ok) {
      userProfile.value = await response.json();
      console.log("User profile:", userProfile.value);
    } else {
      console.error("Failed to fetch profile:", response.status);
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
  <div class="profile-wrapper">
    <NavBar />
    <div class="side-nav">
      <div class="nav-profile">
        <div class="profile-icon">
          {{ userProfile?.user.first_name?.[0]
          }}{{ userProfile?.user.last_name?.[0] }}
        </div>
        <div class="profile-info">
          <h3>
            {{ userProfile?.user.first_name }} {{ userProfile?.user.last_name }}
          </h3>
          <p>{{ userProfile?.user.user_type }}</p>
        </div>
      </div>

      <div class="nav-sections">
        <a href="#personal" class="nav-section active">
          <i class="fas fa-user"></i>
          Personal Information
        </a>
        <a href="#security" class="nav-section">
          <i class="fas fa-shield-alt"></i>
          Security Settings
        </a>
        <a href="#preferences" class="nav-section">
          <i class="fas fa-cog"></i>
          Preferences
        </a>
      </div>
    </div>

    <div class="main-content">
      <div class="profile-content" v-if="userProfile">
        <div class="content-grid">
          <div class="profile-section" id="personal">
            <h2>Personal Information</h2>
            <div class="info-grid">
              <div class="info-item">
                <label>Username</label>
                <p>{{ userProfile.user.user_name }}</p>
              </div>
              <div class="info-item">
                <label>Account Type</label>
                <p>{{ userProfile.user.user_type }}</p>
              </div>
              <div class="info-item">
                <label>First Name</label>
                <p>{{ userProfile.user.first_name }}</p>
              </div>
              <div class="info-item">
                <label>Last Name</label>
                <p>{{ userProfile.user.last_name }}</p>
              </div>
              <div class="info-item full-width">
                <label>Email Address</label>
                <p>{{ userProfile.user.email }}</p>
              </div>
            </div>
          </div>

          <div class="profile-section" id="security">
            <h2>Security Settings</h2>
            <div class="security-options">
              <button class="action-button">
                <i class="fas fa-key"></i>
                Change Password
              </button>
              <button class="action-button">
                <i class="fas fa-shield-alt"></i>
                Two-Factor Authentication
              </button>
            </div>
          </div>

          <div class="profile-section" id="preferences">
            <h2>Preferences</h2>
            <div class="preferences-grid">
              <div class="preference-item">
                <label class="toggle">
                  <input type="checkbox" checked />
                  <span class="slider"></span>
                  <span class="toggle-label">Email Notifications</span>
                </label>
              </div>
              <div class="preference-item">
                <label class="toggle">
                  <input type="checkbox" checked />
                  <span class="slider"></span>
                  <span class="toggle-label">SMS Alerts</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="loading-state">
        <p>Loading profile information...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-wrapper {
  display: flex;
  min-height: 100vh;
  background: var(--bank-blue-dark);
  padding-top: 60px;
}

.side-nav {
  width: 280px;
  background: rgba(26, 35, 126, 0.6);
  backdrop-filter: blur(10px);
  padding: 2rem 1rem;
  border-right: 1px solid var(--bank-gold);
  position: fixed;
  height: calc(100vh - 60px);
}

.nav-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid rgba(207, 181, 59, 0.2);
  width: 100%;
}

.profile-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(
    135deg,
    var(--bank-gold) 0%,
    var(--bank-gold-dark) 100%
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.4rem;
  color: var(--bank-blue-dark);
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.profile-info {
  text-align: center;
  width: 100%;
}

.profile-info h3 {
  color: var(--bank-gold);
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  white-space: normal;
  overflow: visible;
  word-break: break-word;
  line-height: 1.3;
}

.profile-info p {
  color: var(--bank-white);
  opacity: 0.7;
  font-size: 1rem;
  white-space: normal;
  overflow: visible;
  word-break: break-word;
  line-height: 1.3;
}

.nav-sections {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  color: var(--bank-white);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-section:hover,
.nav-section.active {
  background: rgba(207, 181, 59, 0.1);
  color: var(--bank-gold);
}

.nav-section i {
  width: 20px;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 2rem;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-section {
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 1.5rem;
}

.profile-section h2 {
  color: var(--bank-gold);
  font-size: 1.4rem;
  margin-bottom: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  color: var(--bank-white);
  opacity: 0.8;
  font-size: 0.9rem;
}

.info-item p {
  color: var(--bank-white);
  font-size: 1.1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.security-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-button {
  padding: 1rem;
  background: rgba(26, 35, 126, 0.4);
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  color: var(--bank-white);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.action-button:hover {
  background: rgba(207, 181, 59, 0.1);
  transform: translateY(-2px);
}

.preferences-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.preference-item {
  display: flex;
  align-items: center;
}

.toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.toggle-label {
  margin-left: 0.5rem;
  color: var(--bank-white);
}

.slider {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: var(--bank-white);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.toggle input {
  display: none;
}

.toggle input:checked + .slider {
  background-color: var(--bank-gold);
}

.toggle input:checked + .slider:before {
  transform: translateX(20px);
}

.loading-state {
  text-align: center;
  color: var(--bank-white);
  opacity: 0.7;
  padding: 2rem;
}

@media (max-width: 1024px) {
  .side-nav {
    width: 80px;
    padding: 1rem 0.5rem;
  }

  .nav-section span {
    display: none;
  }

  .profile-info {
    display: block;
  }

  .nav-profile {
    flex-direction: column;
  }

  .main-content {
    margin-left: 80px;
  }
}

@media (max-width: 768px) {
  .profile-wrapper {
    flex-direction: column;
  }

  .side-nav {
    width: 100%;
    height: auto;
    position: static;
    padding: 1rem;
  }

  .nav-sections {
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
  }

  .nav-section {
    padding: 0.75rem;
  }

  .main-content {
    margin-left: 0;
    padding: 1rem;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
