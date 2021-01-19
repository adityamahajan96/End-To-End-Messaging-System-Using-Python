import socket 
import select 
import sys 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number") 
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
print("CONNECTED.....")
message = server.recv(2048)
print(message.decode('utf-8'))

#signup = 0
#login = 0
#username = ''
#password = ''

while True: 
	sockets_list = [sys.stdin, server] 
	read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
	#print("Please LOGIN/SIGNUP to continue: ")
	

	#msg = sys.stdin.readline()
	#msg_split = msg.split(' ')
	#if msg_split[0] == 'LOGIN':
	#	server.send(msg)
	#	flag = server.recv(2048)
	#	if flag == '0':
	#		print('INVALID Credentials.. Please try again !!')
	#		continue
	#	else:
	#		print('LOGIN Successful !!')
	#elif msg_split[0] == 'SIGNUP': 
	#	server.send(msg)
	#	flag = server.recv(2048)
	#	if flag == '1':
	#		print('SIGNUP Successful !! Please login to continue...')
	#	else:
	#		print('SIGNUP Failed.. Please try again !!')
	#	continue


	#else:
	#	print('INVALID COMMAND (LOGIN/SIGNUP).. Please try again !!')
	#	continue
	#for socks in read_sockets: 
	#	if socks == server: 
	#		message = socks.recv(2048) 
	#		print (message)
	#		break 
	#	else:
	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			#DECRYPT
			print(message.decode('utf-8'))
		else:
			msg = sys.stdin.readline()
			msg_split = msg.split(' ')

			#print('msg_split: ', msg_split)
			if msg_split[0] == 'LOGIN':
				#if login == 1:
				#	print('Already LOGGED IN with User: <' + username + '>. Please LOGOUT to continue...')
				#	continue
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048)
				if flag == '0':
					print('LOGIN FAILED.. Please try again !!')
					continue
				else:
					print('LOGIN Successful !!')
					#username = msg_split[1]
					#password = msg_split[2]
					#login = 1
			
			elif msg_split[0] == 'LOGOUT\n':
				server.send(bytes(msg, 'utf-8'))
				flag_msg = server.recv(2048)
				if flag_msg.decode('utf-8') != '0':
					print(flag_msg.decode('utf-8'))
				else:
					print('Some LOGOUT Error !! Please try again...')
				
			elif msg_split[0] == 'SIGNUP': 
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048)
				if flag.decode('utf-8') == '1':
					print('SIGNUP Successful !! Please login to continue...')
					#signup = 1
				else:
					print('SIGNUP FAILED.. Please try again !!')
				continue
			
			elif msg_split[0] == 'CREATE':
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048)
				if flag.decode('utf-8') == '0':
					print('FAILURE in GROUP CREATION !!')
				else:
					print(flag.decode('utf-8'))

			elif msg_split[0] == 'LIST\n':
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048)
				if flag.decode('utf-8') == '0':
					print('GROUP_LIST Error !!')
				else:
					print(flag.decode('utf-8'))

			elif msg_split[0] == 'JOIN':
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048)
				if flag.decode('utf-8') == '0':
					print('JOIN_GROUP Error !!')
				else:
					print(flag.decode('utf-8'))

			elif msg_split[0] == 'SEND':
				#ENCRYPT
				server.send(bytes(msg, 'utf-8')) 
			 	
				#sys.stdout.write("<You>") 
				#sys.stdout.write(msg) 
				#sys.stdout.flush()
				#message = sys.stdin.readline() 
			#cmd_split = message.split(' ')
			#("splitted msg: ", cmd_split)
			#if cmd_split[0] == "SEND":
				#server.send(msg) 
				#sys.stdout.write("<You>") 
				#sys.stdout.write(msg) 
				#sys.stdout.flush() 
			#else:
			#	sys.stdout.write("Please enter a valid command...")
			#	continue
	
sys.stdout.write('Exiting...') 				
server.close() 
