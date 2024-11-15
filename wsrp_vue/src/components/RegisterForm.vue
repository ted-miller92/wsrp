<script setup>

</script>

<template>
	<div class="item">
		<div class="details">
			<h3>Register</h3>
			<form>
				<label for="username">Username</label>
				<input type="text" placeholder="username" />
				<label for="password">Password</label>
				<input type="password" placeholder="password" />
                <label for="password">Confirm Password</label>
				<input type="password" placeholder="password" />
                
				<button type="submit">Register</button>
                <p>Already have an account? <router-link to="/login">Login</router-link></p>
			</form>
		</div>	
	</div>	
</template>

<style scoped>
.item {
  margin-top: 2rem;
  display: flex;
  position: relative;
}
.details {
  flex: 1;
  margin-left: 1rem;
}
input {
	display:block;
	margin: 6px 0px 6px 0px;
}
button {
	margin: 6px 12px 6px 0px;
}

h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: var(--color-heading);
}
</style>