import socket
import sys
import json
import os
import thread
import time
import threading

# HOST = '192.168.42.1'
HOST = 'localhost'
PORT = 10000

n = 0
t = 0

quest = 'undefined'
ans = 'undefined'

def giveturn(conn):

	# send update message to client
	if (n == 1):
		msg = "NOW"
	elif (n == 2):
		msg = "WAIT"
	else:
		msg = "EXCEED"

	conn.send(msg)

# client thread function
def clientthread(conn, n):
	lastreq = ''
	while True:
		msg_str = conn.recv(1024)

		global quest
		global ans
		global turn

		if msg_str != lastreq:
			print "CLIENT " + str(n) + " ASK " + msg_str
			lastreq = msg_str

		if (msg_str == "AREDONE"):
			if (quest == 'undefined'):
				conn.send("NOPE")
			else:
				conn.send("GO")

		elif (msg_str == "NEEDRESULT"):
			if (quest == 'undefined'):
				conn.send("NOQUEST")
			elif (ans == 'undefined'):
				conn.send('WAIT')
			else:
				print "Result:",
				if (quest == ans):
					print "menang"
					conn.send("MENANG")
				else:
					print "kalah"
					conn.send("KALAH")

				time.sleep(1)
				quest = 'undefined'
				ans = 'undefined'

		else:
			if (quest == 'undefined'):
				quest = msg_str
				print "Quest:", quest
			elif (ans == 'undefined'):
				ans = msg_str
				print "Answer:", ans 

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