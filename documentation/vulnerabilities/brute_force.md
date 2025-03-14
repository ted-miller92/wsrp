---
id: brute-force
---

## Brute Force

A brute force attack is a method of attempting to gain unauthorized access to a system by systematically trying all possible combinations of usernames and passwords until the correct one is found. In this project, we demonstrate both a vulnerable endpoint that allows unlimited login attempts and a secure endpoint with proper protections against brute force attacks.

### 1. Insecure Login Endpoint (/insecure_login)
This route is a basic, insecure login endpoint without any password hashing, rate-limiting, or brute-force protection. It checks if the provided credentials (username and password) match those stored in the database.

What it does:

Accepts a POST request with a JSON body containing username and password.
Queries the users table in the database to check if the provided username exists.
If the username is found and the password matches (no hashing), the login is successful.
If the credentials don't match, it returns a 401 Unauthorized error.
Thunder Client Test:

Set the request method to POST.
Enter the URL of your server, e.g., http://localhost:5000/insecure-login.
In the Body tab, select JSON and enter the following example data:
json
Copy
Edit
{
  "username": "test_user",
  "password": "password123"
}
Hit Send.
If credentials match the database, you'll receive a 200 response with the message Login successful.
If the credentials are incorrect, you'll get a 401 error with the message Invalid credentials.
With no rate limiting in place, you can send this request as many times as possible (brute force until getting a right password can be demonstrated later with BurpSuite). 

---

### 2. Secure Login Endpoint with Brute-force Protection (/secure_login)
This route applies rate-limiting and brute-force protection to secure the login process. It uses Flask-Limiter for rate-limiting and tracks failed login attempts per user.

What it does:

Accepts a POST request with username and password in the request body.
Fetches the stored password hash for the username from the database and compares it with the provided password (using bcrypt hashing).
Implements brute-force protection by:
Limiting the number of login attempts to 3 per minute via rate-limiting.
Tracking failed login attempts per user and introducing an artificial delay (5 seconds) if there are 3 or more failed attempts.
Adding a random delay (1-3 seconds) to prevent timing attacks.
Thunder Client Test:

Set the request method to POST.
Enter the URL: http://localhost:5000/secure_login.
In the Body tab, select JSON and enter the following example data:
json
Copy
Edit
{
  "username": "test_user",
  "password": "password123"
}
Hit Send.
If credentials are correct, you'll get a 200 response with Login successful.
If incorrect, the response will be a 401 error with Invalid credentials.
!!!After three failed attempts from the same IP, you will see a 403 error with the message Too many failed attempts. Try again later..!!!

---

### 3. Reset Failed Attempts Endpoint (/reset_failed_attempts)
This endpoint allows you to reset the failed login attempts for a specific user. It can be useful to reset the counter after an account lockout due to too many failed login attempts.

What it does:

Accepts a POST request with the username whose failed attempts you want to reset.
Removes the specified user's entry from the failed_attempts dictionary, which tracks failed login attempts.
Thunder Client Test:

Set the request method to POST.
Enter the URL: http://localhost:5000/reset_failed_attempts.
In the Body tab, select JSON and enter the following example data:
json
Copy
Edit
{
  "username": "test_user"
}
Hit Send.
If the user has failed login attempts, they will be cleared, and the response will be: Failed attempts for test_user have been reset.
If no failed attempts exist for the username, you'll still receive the same success message, but the dictionary won’t have the username's entry anymore.


Rate-Limiting and Brute-Force Protection Overview
Rate-Limiting: The secure_login endpoint uses Flask-Limiter to restrict the number of login attempts from the same IP address to 3 per minute. This helps prevent automated attacks and protects your server from being overwhelmed by too many requests.

Brute-Force Protection: Failed login attempts are tracked per user. If a user has failed 3 or more attempts, further attempts from that user will be delayed by 5 seconds (to discourage rapid guessing). This is to prevent brute-force attacks where an attacker might try a lot of passwords in quick succession.

Bcrypt Password Hashing: In the secure_login route, bcrypt is used to compare the hashed password in the database with the password provided by the user. This makes the login more secure, as plaintext passwords are never stored.

Expected Behavior When Testing with Thunder Client
Insecure Login:

Correct credentials: Returns Login successful.
Incorrect credentials: Returns Invalid credentials.
Secure Login:

Correct credentials: Returns Login successful if the username and password match.
Incorrect credentials: Returns Invalid credentials.
Exceeding failed attempts: If there are 3 failed attempts, the response will be a 403 with the message Too many failed attempts. Try again later..
Reset Failed Attempts:

Resets the failed login attempts for the specified user.
Final Notes:
Ensure that your local server is running and accessible on the given port (e.g., localhost:5000).
Test edge cases, such as sending empty or malformed data to see how your app handles errors.
You can test rate-limiting by attempting to hit the secure login endpoint multiple times in quick succession from the same IP.

---

### Why This Is Dangerous

Brute force vulnerabilities can be particularly dangerous because:
- Attackers can systematically discover valid user credentials
- Modern computing power makes it feasible to try thousands of combinations quickly
- Once credentials are discovered, attackers gain legitimate access to accounts
- Automated tools can run 24/7 until successful
- Common password patterns make some accounts especially vulnerable

The impacts can include:
- Unauthorized access to user accounts
- Theft of sensitive information
- Financial losses
- Identity theft
- Compromise of entire systems through admin account access
- Reputation damage to the organization
- Mask other malicious activities

The secure version of any login system should implement:
- Rate limiting
- Account lockouts
- Strong password requirements
- Multi-factor authentication where possible
- Logging and monitoring of failed attempts
