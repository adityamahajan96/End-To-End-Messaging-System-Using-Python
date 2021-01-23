import socket 
import select 
import sys 
import tqdm
import os
from Crypto.Cipher import DES3
from Crypto import Random
from random import randint
from time import *

def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

key = b'Sixteen_byte_key'
G = 9
P = 23
a = 0


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number") 
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 

message = server.recv(2048).decode()
print(message)

SEPARATOR = "<FALTU>"
BUFFER = 4096

username = ''

while True: 
	sockets_list = [sys.stdin, server] 
	read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
	
	for socks in read_sockets:
		if socks == server:
			act = server.recv(2048)
			act_split = act.split(b'<SEPARATOR>')
			#print('act_split: ', act_split)
			if str(act_split[2])[2:-1] == 'GROUP':
				y = int(str(act_split[5])[2:-1])
			else:
				y = int(str(act_split[3])[2:-1])
			#print('Received y:', y)
			
			key2 = int(pow(y, a, P))
			if key2 == 1:
				key2 += 5
			#print('key2:', key2)

			temp = []
			for i in range(16):
				b = (key2 >> (i * 8)) & 0xFF
				temp.append(b)
			#print('temp:', temp)

			temp2 = [chr(b) for b in temp]
			
			key2_main = bytearray(b'')
			for i in temp2:
				key2_main.extend(bytes(i, 'utf-8'))
			
			#print('key: ', key2_main)
			cipher_decrypt = DES3.new(key2_main, DES3.MODE_OFB, act_split[0])
			decrypted_text = cipher_decrypt.decrypt(act_split[1])
			if str(act_split[2])[2:-1] == 'GROUP':
				print('<' + str(act_split[3])[2:-3] + '><' + str(act_split[4])[2:-1] + '>: ' + str(decrypted_text)[2:-1].strip())
			else:
				print('<' + str(act_split[2])[2:-1] + '>: ' + str(decrypted_text)[2:-1].strip())
			continue
		else:
			msg = sys.stdin.readline()
			#print(msg.split(' '))
			msg2_split = msg.split(' ')
			msg2 = ''
			for i in range(0, len(msg2_split)):
				msg2 += msg2_split[i] + '<SEPARATOR>'
			msg = msg2[:-11]
			msg_split = msg2.split('<SEPARATOR>')
			msg_split.pop()
			#print(msg_split)
			
			if msg_split[0] == 'LOGIN':
				username = msg_split[1]
				
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048).decode()
				if flag == '0':
					print('LOGIN FAILED.. Please try again !!')
					continue
				else:
					print('LOGIN Successful !!')
					a = randint(0, 999999) + 2020202018
					x = int(pow(G, a, P))
					server.send(bytes('X<SEPARATOR>' + str(x) + '<SEPARATOR>faltu', 'utf-8'))
				
			elif msg_split[0] == 'LOGOUT\n':
				username = ''
				server.send(bytes(msg, 'utf-8'))
				flag_msg = server.recv(2048).decode()
				if flag_msg != 0:
					print(flag_msg)
				else:
					print('Some LOGOUT Error !! Please try again...')
				
			elif msg_split[0] == 'SIGNUP': 
				username = msg_split[1]
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048).decode()
				if flag == '1':
					print('SIGNUP Successful !! Please login to continue...')
				else:
					print('SIGNUP FAILED.. Please try again !!')
				continue
			
			elif msg_split[0] == 'CREATE':
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048).decode()
				if flag == '0':
					print('FAILURE in GROUP CREATION !!')
				else:
					print(flag)

			elif msg_split[0] == 'LIST\n':
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048).decode()
				if flag == '0':
					print('GROUP_LIST Error !!')
				else:
					print(flag)      

			elif msg_split[0] == 'JOIN':
				server.send(bytes(msg, 'utf-8'))
				flag = server.recv(2048).decode()
				if flag == '0':
					print('JOIN_GROUP Error !!')
				else:
					print(flag)

			elif msg_split[0] == 'EXIT\n':
				username = ''
				server.send(bytes('LOGOUT\n', 'utf-8'))
				flag_msg = server.recv(2048).decode()
				if flag_msg != 0:
					print(flag_msg)
				else:
					print('Some LOGOUT Error !! Please try again...')
				sys.exit()


			elif msg_split[0] == 'SEND':
				#ENCRYPT
				server.send(bytes('CHECK<SEPARATOR>' + msg_split[1] + '<SEPARATOR>' + username + '<SEPARATOR>faltu', 'utf-8'))
				chk_flg = server.recv(2048).decode()
				chk_flg_s = chk_flg.split('<SEPARATOR>')

				if chk_flg_s[0] == 'YES_GROUP':
					all_x = chk_flg_s[1].split('<SEP>')
					all_uname = chk_flg_s[2].split('<SEP>')
					#print('all_x:', all_x)
					#print('all_uname:', all_uname)
					for i2 in range(0, len(all_x) - 1):
						sleep(1)
						server.send(bytes('SEND<SEPARATOR>' + all_uname[i2] + '<SEPARATOR>faltu3', 'utf-8'))
						flag = server.recv(2048).decode()
						
						if msg_split[2] == 'FILE':
							server.send(b'FILE')
							f = server.recv(2048).decode()
							
							filename = msg_split[3][:-1]
							filesize = os.path.getsize(filename)
							server.send(f"{filename}{SEPARATOR}{filesize}".encode())
							
							tmp_var = 0
							with open(filename, "rb") as f:
								while True:
									bytes_read = f.read(BUFFER)
									if not bytes_read:
										break
									server.sendall(bytes_read)
									tmp_var += 1
							if tmp_var == 0:
								print('Unable to send file !!')
							else:
								print('FILE SENT SUCCESSFULLY !!')
							
						else:
							server.send(b'MSG')
							f = server.recv(2048).decode()
							actual = ''
							for i in range(2, len(msg_split)):
								actual += msg_split[i] + ' '
							actual = actual.strip()
							
							iv = Random.new().read(DES3.block_size)

							y = int(all_x[i2])
							#print('received x: ', y)
							key1 = int(pow(y, a, P))
							if key1 == 1:
								key1 += 5
							#print('key1:', key1)

							temp = []
							for i in range(16):
								b = (key1 >> (i * 8)) & 0xFF
								temp.append(b)
							#print('temp:', temp)

							temp2 = [chr(b) for b in temp]
							key1_main = bytearray(b'')
							for i in temp2:
								key1_main.extend(bytes(i, 'utf-8'))

							#print('key1_main: ', key1_main)
							cipher_encrypt = DES3.new(key1_main, DES3.MODE_OFB, iv)

							
							actual_msg = pad(actual)
							encrypted_text = cipher_encrypt.encrypt(bytes(actual_msg, 'utf-8'))

							total = bytearray(iv)
							total.extend(b'<SEPARATOR>')
							total.extend(encrypted_text)
							total.extend(b'<SEPARATOR>GROUP<SEPARATOR>')
							total.extend(bytes(chk_flg_s[3], 'utf-8'))
							#print(encrypted_text)
							#print('total:', total)
							server.send(total)

				elif chk_flg_s[0] == 'YES':
					server.send(bytes('SEND<SEPARATOR>' + msg_split[1] + '<SEPARATOR>faltu2', 'utf-8'))
					flag = server.recv(2048).decode()
					
					if msg_split[2] == 'FILE':
						server.send(b'FILE')
						f = server.recv(2048).decode()
						
						filename = msg_split[3][:-1]
						filesize = os.path.getsize(filename)
						server.send(f"{filename}{SEPARATOR}{filesize}".encode())
						
						tmp_var = 0
						with open(filename, "rb") as f:
							while True:
								bytes_read = f.read(BUFFER)
								if not bytes_read:
									break
								server.sendall(bytes_read)
								tmp_var += 1
						if tmp_var == 0:
							print('Unable to send file !!')
						else:
							print('FILE SENT SUCCESSFULLY !!')
						
					else:
						server.send(b'MSG')
						f = server.recv(2048).decode()
						actual = ''
						for i in range(2, len(msg_split)):
							actual += msg_split[i] + ' '
						actual = actual.strip()
						
						iv = Random.new().read(DES3.block_size)

						y = int(chk_flg_s[1])
						#print('received x: ', y)
						key1 = int(pow(y, a, P))
						if key1 == 1:
							key1 += 5
						#print('key1:', key1)

						temp = []
						for i in range(16):
							b = (key1 >> (i * 8)) & 0xFF
							temp.append(b)
						#print('temp:', temp)

						temp2 = [chr(b) for b in temp]
						key1_main = bytearray(b'')
						for i in temp2:
							key1_main.extend(bytes(i, 'utf-8'))

						#print('key1_main: ', key1_main)
						cipher_encrypt = DES3.new(key1_main, DES3.MODE_OFB, iv)

						
						actual_msg = pad(actual)
						encrypted_text = cipher_encrypt.encrypt(bytes(actual_msg, 'utf-8'))

						total = bytearray(iv)
						total.extend(b'<SEPARATOR>')
						total.extend(encrypted_text)
						#print(encrypted_text)
						#print('total:', total)
						server.send(total)
												
				else:
					print('INVALID USERNAME/GROUP NAME !!')
					continue
			else:
				print('PLEASE ENTER A VALID COMMAND...')
			 	
sys.stdout.write('Exiting...') 				
server.close() 
