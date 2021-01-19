import socket 
import select 
import sys 
import threading

class users:
	def __init__(self, ip, port, username, password, conn, login):
		self.ip = ip
		self.port = port
		self.username = username
		self.password = password
		self.conn = conn
		self.login = login
		self.groups = []

class groups:
	def __init__(self, group_name, owner):
		self.group_name = group_name
		self.owner = owner
		self.group_members = []
		self.mem_count = 1

user_list = []
group_list = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number") 
	exit() 

IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 

server.bind((IP_address, Port)) 
server.listen(100) 

list_of_clients = [] 

def conn_to_user(conn):
	for u in user_list:
		if u.conn == conn:
			return u.username

def msg_combine(conn, msg_split):
	msg = '<' + conn_to_user(conn) + '>: '
	for m in range(2, len(msg_split)):
		msg += msg_split[m] + ' '
	return msg

def msg_combine2(conn, msg_split):
	msg = '<' + conn_to_user(conn) + '>: '
	for m in range(1, len(msg_split)):
		msg += msg_split[m] + ' '
	return msg

def grp_msg_combine(conn, msg_split, grp):
	msg = '<' + grp + '><' + conn_to_user(conn) + '>: '
	for m in range(2, len(msg_split)):
		msg += msg_split[m] + ' '
	return msg

def clientthread(conn, addr): 
	conn.send(bytes("## Welcome to Terminal-Whatsapp ##", 'utf-8'))
	while True: 
		#try: 	
			message = conn.recv(2048)

			#print(message.decode('utf-8'))

			msg_split = message.decode('utf-8').split(' ')

			if msg_split[0] == 'SIGNUP':
				fl = 0
				for usr in user_list:
					if usr.username == msg_split[1]:
						fl = 1 
						break
				if fl == 0:
					u = users(addr[0], addr[1], msg_split[1], msg_split[2], conn, 0)
					user_list.append(u)
					conn.send(bytes('1', 'utf-8'))
					continue
				else:
					conn.send(bytes('0', 'utf-8'))

			if msg_split[0] == 'LOGIN':
				fl = 0
				for usr in user_list:
					if msg_split[1] == usr.username and msg_split[2] == usr.password and usr.login == 0:
						usr.login = 1
						usr.conn = conn
						print("User: <" + usr.username + "> Logged in !!")
						fl = 1
						conn.send(bytes('1', 'utf-8'))
						break
				if fl == 0:
					conn.send(bytes('0', 'utf-8'))
					continue

			if msg_split[0] == 'LOGOUT\n':
				fl = 0
				for usr in user_list:
					if conn == usr.conn and usr.login == 1:
						usr.login = 0
						print('<' + usr.username + '> LOGGED OUT !!')
						conn.send(bytes('<' + usr.username + '> LOGGED OUT Successfully !!', 'utf-8'))
						#conn.send('1')
						fl = 1
						break
				if fl == 1:
					continue
				else:
					print('<' + usr.username + '> LOGOUT ERROR...')
					conn.send(bytes('0', 'utf-8'))

			if msg_split[0] == 'CREATE':
				fl = 0
				for g in group_list:
					if g.group_name == msg_split[1]:
						fl = 1
						conn.send(bytes('0', 'utf-8'))
						break
				if fl == 0:
					fl2 = 0
					for usr in user_list:
						if usr.conn == conn and usr.login == 1:
							gr = groups(msg_split[1], usr.username)
							gr.group_members.append(usr.username)
							group_list.append(gr)
							usr.groups.append(msg_split[1][:-1])
							conn.send(bytes('Group <' + msg_split[1][:-1] + '> CREATED Successfully !!', 'utf-8'))
							fl2 = 1
							break
					if fl2 == 0:
						conn.send(bytes('0', 'utf-8'))

			if msg_split[0] == 'LIST\n':			
				fl = 0
				for usr in user_list:
					if usr.conn == conn and usr.login == 1:
						fl = 1
						break
				if fl == 0:
					conn.send(bytes('0', 'utf-8'))
					continue
				else:
					msg = 'GROUP_NAME\tOWNER\tMEMBERS\tMEMBER_COUNT\n'
					for g in group_list:
						msg2 = ''
						for mem in g.group_members:
							msg2 += mem + ', '
						msg += g.group_name[:-1] + '\t\t' + g.owner + '\t(' + msg2 + ')\t' + str(g.mem_count) + '\n'
					conn.send(bytes(msg, 'utf-8'))

			if msg_split[0] == 'JOIN':
				fl = 0
				for usr in user_list:
					if usr.conn == conn and usr.login == 1:
						fl = 1
						break
				if fl == 0:
					conn.send(bytes('0', 'utf-8'))
					continue
				else:
					fl2 = 0
					for g in group_list:
						if msg_split[1] == g.group_name:
							fl2 = 1
							usr = ''
							for u2 in user_list:
								if u2.conn == conn:
									u2.groups.append(g.group_name[:-1])
									usr = u2.username
									break
							g.group_members.append(usr)
							g.mem_count += 1

							conn.send(bytes('You joined the group <' + g.group_name[:-1] + '> Successfully !!', 'utf-8'))
							break
					if fl2 == 0:
						conn.send(bytes('0', 'utf-8'))

			if msg_split[0] == 'SEND':
				fl3 = 0
				for u in user_list:
					if u.conn == conn and u.login == 1:
						print ("<" + u.username + ">: " + message.decode('utf-8'))
						"""fl2 = 0
						for usr in user_list:
							if msg_split[1] == usr.username and usr.login == 1:
								main_message = msg_combine(conn, msg_split)
								usr.conn.send(main_message)
								fl2 = 1
								break
						if fl2 == 0:
							fl4 = 0
							for g in group_list:
								if msg_split[1] == g.group_name[:-1]:
									demo_u = ''
									for u4 in user_list:
										if u4.conn == conn:
											demo_u = u4.username
											break
									fl4 = 1
									group_conn_list = []
									fl7 = 0
									if demo_u in g.group_members:
										for u3 in user_list:
											if u3.username in g.group_members:
												group_conn_list.append(u3.conn)
									else:
										fl7 = 1
										break
									multicast(grp_msg_combine(conn, msg_split, g.group_name[:-1]), conn, group_conn_list)
									break
							if fl4 == 0 and fl7 == 0:
								conn.send('FAILURE in sending Group Message !!')
							elif fl7 == 1:
								conn.send('MESSAGE NOT SENT !! You are NOT a member of <' + g.group_name[:-1] + '>')"""
										
							#main_message = msg_combine(conn, msg_split)
							#broadcast(main_message, conn)
						fl2 = 0
						for usr in user_list:
							if msg_split[1] == usr.username and usr.login == 1:
								fl2 = 1
								if msg_split[2] == 'FILE':
									pass
								else:
									main_message = msg_combine(conn, msg_split)
									usr.conn.send(bytes(main_message, 'utf-8'))
								break
						if fl2 == 0:
							usr_list = []
							fl8 = 0
							for usr in user_list:
								if usr.conn == conn:
									fl8 = 1
									for gm in usr.groups:
										for gt in group_list:
											if gt.group_name[:-1] == gm:
												for i in gt.group_members:
													usr_list.append(i)
									break			
							final_conn_list = []
							for u4 in user_list:
								for u5 in usr_list:
									if u4.username == u5:
										final_conn_list.append(u4.conn)
										break
							conn_tuple = tuple(final_conn_list)
							multicast(msg_combine2(conn, msg_split), conn, conn_tuple)
						fl3 = 1
						break
				if fl3 == 0:
					conn.send(bytes('Please SIGNUP/LOGIN to SEND messages...', 'utf-8'))

def multicast(msg, conn, group_conn_list):
	#print('Inside MULTICAST !!')
	for mem_conn in group_conn_list: 
		if mem_conn != conn: 
			try: 
				mem_conn.send(bytes(msg,'utf-8')) 
			except: 
				print('MULTICAST error !!')
				mem_conn.close() 
				remove(mem_conn) 

def multicast2(msg, conn, group_conn_tuple):
	#print('Inside MULTICAST !!')
	for mem_conn in group_conn_tuple: 
		if mem_conn != conn: 
			try: 
				mem_conn.send(bytes(msg,'utf-8')) 
			except: 
				print('MULTICAST error !!')
				mem_conn.close() 
				remove(mem_conn) 

def broadcast(message, connection): 
	#print('Inside broadcast !!')
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(bytes(message,'utf-8')) 
			except: 
				print('broadcast error !!')
				clients.close() 
				remove(clients) 

def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 

#client_no = 0
while True: 
	#client_no += 1
	conn, addr = server.accept() 
	list_of_clients.append(conn) 
	print ("<" + addr[0] + "><" + str(addr[1]) + "> connected") 
	cThread = threading.Thread(target = clientthread, args = (conn, addr))
	cThread.daemon = True
	cThread.start()

conn.close() 
server.close() 
