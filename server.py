import socket
import sys
import json
import os
import thread
import time
import threading
import subprocess

HOST = '192.168.42.1'
# HOST = 'localhost'
PORT = 10000

n = 0
t = 0

quest = 'undefined'
ans = 'undefined'
delay = 2

def giveturn(conn):

	# send update message to client
	if (n == 1):
		msg = "NOW"
	elif (n == 2):
		msg = "WAIT"
	else:
		msg = "EXCEED"

	conn.send(msg)

def lightemup(str):
	for c in str:
		if c.upper() == 'K':
			subprocess.call('./gpio9.sh', shell=True)
		elif c.upper() == 'M':
			subprocess.call('./gpio10.sh', shell=True)
		elif c.upper() == 'H':
			subprocess.call('./gpio11.sh', shell=True)


# client thread function
def clientthread(conn, n):
	lastreq = ''
	while True:
		msg_str = conn.recv(1024)

		global quest
		global ans
		global turn
		global delay

		if msg_str != lastreq:
			print "CLIENT " + str(n) + " ASK " + msg_str
			lastreq = msg_str

		if (msg_str == "AREDONE"):
			if (quest == 'undefined'):
				conn.send("NOPE")
			else:
				time.sleep(len(quest)+1)
				conn.send("GO")

		elif (msg_str == "NEEDRESULT"):
			if (quest == 'undefined'):
				conn.send("NOQUEST")
			elif (ans == 'undefined'):
				conn.send('WAIT')
			else:
				#global delay
				time.sleep(delay)
				delay = 0
				print "Result:",
				if (quest == ans):
					print "menang"
					conn.send("MENANG")
				else:
					print "kalah"
					conn.send("KALAH")

				#time.sleep(8)
				quest = 'undefined'
				ans = 'undefined'

		else:
			if (quest == 'undefined'):
				quest = msg_str
				print "Quest:", quest
			elif (ans == 'undefined'):
				ans = msg_str
				delay = len(ans)+1
				print "Answer:", ans
			lightemup(msg_str)

# main program starts here
if __name__ == "__main__":

	try:
		
		# create socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		# bind
		s.bind((HOST, PORT))

		# listen
		s.listen(10)
		print 'Server opened on on host', HOST, 'port ' + str(PORT)
		print 'Server ready, now listening ...'

		# response request
		while True:
			conn, addr = s.accept()
			n += 1
			print 'Connection n = ' + str(n) + ' from ' + addr[0] + ':' + str(addr[1])

			giveturn(conn)

			# create thread 
			thread.start_new_thread(clientthread, (conn,n))

	except socket.error, msg:
		if msg[0] == 13:
			print "Error: Port is unusable.\n"
		elif msg[0] == 99:
			print "Error: Cannot assign requested host.\n"
	except ValueError:
		print "Error: Port must be a number.\n"
	except KeyboardInterrupt:
		print('\nKeyboard interrupt detected. Exiting gracefully...\n')
		quit()
