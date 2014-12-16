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

flag = False
getter = -1

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
			onesec(9)
		elif c.upper() == 'M':
			onesec(10)
		elif c.upper() == 'H':
			onesec(11)	

def onesec(arg):
	num = str(arg)
	subprocess.call('./lightgpio.sh 1 ' + num, shell=True)
	time.sleep(1)
	subprocess.call('./lightgpio.sh 0 ' + num, shell=True)

def we_got_winner():
	subprocess.call('./lightgpio.sh 1 17', shell=True)
	for _ in xrange(3):
		for i in xrange(2):
			arg = str(1-i)
			subprocess.call('./lightgpio.sh '+arg+' 10', shell=True)
			time.sleep(0.01)
			subprocess.call('./lightgpio.sh '+arg+' 9', shell=True)
			time.sleep(0.01)
			subprocess.call('./lightgpio.sh '+arg+' 11', shell=True)
			time.sleep(0.01)
	time.sleep(1)
	subprocess.call('./lightgpio.sh 0 17', shell=True)

def no_winner():
	subprocess.call('./lightgpio.sh 1 22', shell=True)
	time.sleep(2)
	subprocess.call('./lightgpio.sh 0 22', shell=True)

# client thread function
def clientthread(conn, n):
	lastreq = ''
	while True:
		msg_str = conn.recv(1024)

		global quest
		global ans
		global flag
		global getter

		if msg_str != lastreq:
			print "CLIENT " + str(n) + " ASK (" + msg_str + ")"
			lastreq = msg_str

		if (msg_str == ''):
			print "Lost connection from client " + str(n) + "!"
			break

		if (msg_str == "AREDONE"):
			if (quest == 'undefined'):
				conn.send("NOPE")
			else:
				time.sleep(len(quest)+1)
				conn.send("GO")

		elif (msg_str == "NEEDRESULT"):
			if getter == -1 and not flag:
				getter = n
				flag = True

			if (quest == 'undefined'):
				conn.send("NOQUEST")
			elif (ans == 'undefined'):
				conn.send('WAIT')
			else:
				if n == getter:
					time.sleep(len(ans)+1)

				print "Result "+str(n)+":",
				if (quest == ans):
					print "menang"
					we_got_winner()
					conn.send("MENANG")
				else:
					no_winner()
					print "kalah"
					conn.send("KALAH")

				quest = 'undefined'
				ans = 'undefined'
				getter = -1
				flag = False

		else:
			if (quest == 'undefined'):
				quest = msg_str
				print "Quest:", quest
			elif (ans == 'undefined'):
				ans = msg_str
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
		print 'LIGHT \'EM UP SERVER IS RUNNING!'
		print 'Server opened on on host', HOST, 'port ' + str(PORT)
		print 'Server ready, now listening...'

		# response request
		while True:
			conn, addr = s.accept()
			n += 1
			print 'Connection n = ' + str(n) + ' from ' + addr[0] + ':' + str(addr[1])

			giveturn(conn)
			
			if n == 1:
				subprocess.call('./lightgpio.sh 1 23', shell=True)
			else:
				subprocess.call('./lightgpio.sh 1 24', shell=True)

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
		subprocess.call('./lightgpio.sh 0 23', shell=True)
		subprocess.call('./lightgpio.sh 0 24', shell=True)
		quit()
