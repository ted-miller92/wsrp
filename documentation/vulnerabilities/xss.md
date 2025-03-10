---
id: xss
---

## Cross-site Scripting (XSS)

Cross-site Scripting (XSS) occurs when an application takes untrusted data and sends it to a web browser without proper validation or sanitization. In this project, we demonstrate a reflected XSS vulnerability where user input from a login form is directly embedded into the response HTML without sanitization.

### Vulnerable Implementation

The project includes both frontend and backend components that demonstrate XSS:

1. **Backend Endpoint** (`/api/xss_vuln/auth/login`):
   - Takes username/password in a POST request
   - Returns the user input directly in the response without sanitization
   - Even on failed login attempts, reflects back user input

2. **Frontend Component** (`XSSVulnerableForm.vue`):
   - Provides a login form interface
   - Takes the server response and directly injects it into the DOM
   - Creates a demonstration popup showing the vulnerability


### Testing the Vulnerability

To test the XSS vulnerability:

1. Navigate to the XSS Vulnerable Login form
2. In the username field, enter a malicious payload, for example:
```html
<script>alert('XSS Attack!')</script>
```
or
```html
<img src="x" onerror="alert('XSS Vulnerability Detected!')">
```

3. Submit the form with any password
4. The application will reflect back your input and execute any injected JavaScript

---

### Why This Is Dangerous

The XSS vulnerability in this implementation could allow attackers to:
- Steal user session cookies
- Capture user credentials
- Perform actions on behalf of the user
- Redirect users to malicious websites
- Deface the website content

---

### Secure Implementation

To prevent XSS attacks:
1. Always sanitize user input before reflecting it back
2. Use content security policies (CSP)
3. Encode special characters in user input
4. Use modern framework's built-in XSS protections
5. Never directly inject user input into the DOM

The secure version of the login endpoint should sanitize all user inputs and use proper content encoding before sending responses.