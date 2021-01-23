# End-To-End-Messaging-System-Using-Python
- Python3 compatible now.
- End-to-end encryption using 3DES and Diffie-Hellman Key exchange has been implemented for text messages.
- *FILE SHARING part is still pending*
- **SERVER**: python3 server.py 127.0.0.1 <ANY_FREE_PORT>
- **CLIENT**: python3 client.py <SAME_IP_AS_ABOVE> <SAME_PORT_AS_ABOVE>
  
# Commands:
- SIGNUP (username) (password)
- LOGIN (username) (password)
- LOGOUT
- CREATE (group_name)
- JOIN (group_name)
- LIST
- SEND (username) (message)
- SEND (group_name) (message)            *//for Group Broadcasting*
- EXIT
