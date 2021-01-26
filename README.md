# End-To-End-Messaging-System-Using-Python

- **SERVER**: python server.py 127.0.0.1 <ANY_FREE_PORT>
- **CLIENT**: python client.py <SAME_IP_AS_ABOVE> <SAME_PORT_AS_ABOVE>
  
# Commands:
- SIGNUP (username) (password)
- LOGIN (username) (password)
- LOGOUT
- CREATE (group_name)
- JOIN (group_name)
- LIST
- SEND (username/group_name) (message)
- SEND (username/group_name) FILE (relative FILEPATH) 
//NOTE: relative filepath is the home directory (including filename) from where client.py is executed. So, for example, if *client.py* is executed from **TMP** and  if some image *pic.jpg* is present in its child directory **TMP/images**, then the command will be: **SEND (username/group_name) FILE images/pic.jpg**
