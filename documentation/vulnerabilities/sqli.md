---
id: sqli
---

## SQL Injection

'''General info about SQL injection here'''

Here is a request that takes advantage of an endpoint in the server that is vulnerable to SQL injection:

<p align="center">
  <img src="../images/sql_1.png">
</p>

This example is convuluted and obviously staged, but it shows how an attacker may be able to insert characters into a request to manipulate the SQL query that the server is running. In this case, the attacker is able to insert a ' character into the request, which causes the SQL query to be malformed. The attacker can then use this to manipulate the query to return all of the users in the database, which is a huge security risk.