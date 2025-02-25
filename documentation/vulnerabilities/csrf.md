---
id: csrf
---

## Cross-Site Request Forgery (CSRF)

A few things have to be true for CSRF to be possible:
- The user (victim) must be logged in (authenticated) to the target website
- The target website uses cookie based session management
- Request parameters (handled by the website) must be somewhat predictable.

The attacker sends a link to the victim which contains a hidden request to the server. When the victim clicks the link, the request is sent to the target website, "hijacking" the victim's session to make an authenticated request. 

<p align="center">
  <img src="./images/csrf_1.png">
</p>

The request may have hidden parameters that the attacker can control, such as a request to change the user's (victim's) email address to that of the attacker. 


If this request is sent successfully, the attacker can then try to log in to the victim's account to request a password change. After this, the attacker basically has full access to whatever the victim has access to.

To try this out on your own...

### Testing the Insecure Endpoint
The insecure endpoint (/api/csrf_vuln_transfer) is designed to simulate a vulnerable money transfer that does not use CSRF protection. To test this endpoint, you can use tools like Thunder Client or Postman to send a POST request to /api/csrf_vuln_transfer.

Prepare the Request: Open Thunder Client or Postman, and create a new POST request. The URL will be the base of your application followed by /api/csrf_vuln_transfer. For example, http://localhost:5000/api/csrf_vuln_transfer if you're testing locally.

Set the Request Body: In the request body, choose JSON format, and include the following data:

json
Copy
Edit
{
    "from_account": 1,
    "to_account": 2,
    "amount": 100
}
This represents transferring 100 units of currency from account 1 to account 2.

Send the Request: Once the request is prepared, click on "Send" to submit the request. Since the insecure endpoint does not require a CSRF token, it should successfully process the transaction.

Verify the Response: If everything is working correctly, you should receive a response with a 200 status code and a message like:

json
Copy
Edit
{
    "message": "Transfer successful",
    "status_code": 200
}
This means the endpoint is functioning as expected, without any CSRF protection.

---

### Testing the Secure Endpoint
The secure endpoint (/api/secure_transfer) is designed to simulate a money transfer with CSRF protection in place. To test this endpoint, you need to include a CSRF token in your request.

Fetch the CSRF Token: The CSRF token is typically issued after you log into your application or access a page where the token is included in the cookies. Since your login system isn’t working, you could either temporarily disable CSRF protection or mock a CSRF token for testing.

Prepare the Request: Similar to the insecure endpoint, open Thunder Client or Postman and create a new POST request, but this time to /api/secure-transfer. The URL will be something like http://localhost:5000/api/secure_transfer.

Set the Request Body: In the request body, use the same format as for the insecure endpoint:

json
Copy
Edit
{
    "from_account": 1,
    "to_account": 2,
    "amount": 100
}
Add the CSRF Token to the Headers: Go to the "Headers" tab and add a new header:

Key: X-CSRFToken
Value: <your_CSRF_token>
This will simulate sending the CSRF token from your browser’s session. If you have manually retrieved a token or temporarily disabled CSRF protection, this step will ensure the server recognizes the token.

Send the Request: Click on "Send" to submit the request. If the CSRF token is valid and matches the one expected by the server, the transfer should be processed successfully.

Verify the Response: If the request is successful, you should receive a response like:

json
Copy
Edit
{
    "message": "Secure transfer successful",
    "status_code": 200
}
If the CSRF token is missing or invalid, the server should respond with a 400 or 403 status code, indicating that the CSRF token was either not provided or not valid.