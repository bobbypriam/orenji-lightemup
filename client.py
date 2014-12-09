import socket
import sys
import json
import os
import time

HOST = ''
PORT = 8888

turn = True;

s = None

def getturn():
	response = s.recv(1024)
	print response
	if (response == "WAIT"):
		print "Get Second turn ..."
		return False
	elif (response == "NOW"):
		print "Get First turn ..."
		return True
	else:
		s.close()
		quit()

def sendanswer():
	while True:
		print "Waiting ..."

		s.send("AREDONE")
		response = s.recv(1024)

		if (response == "GO"):
			print "Now Answer!"
			break

		time.sleep(0.5)

	userinput = raw_input("Masukkan kombinasi jawaban warna K,M,H")
	s.send(userinput)

def sendquest():
	userinput = raw_input("Masukkan kombinasi warna K,M,H")
	s.send(userinput)

def menang():
	print "MUSUH ANDA COPO!"

def kalah():
	print "ANDA COPO!"

def getresult():
	while True:
		global turn
		s.send("NEEDRESULT")

		response = s.recv(1024)
		v = True
		if (response == "MENANG"):
			v = True
		elif (response == "KALAH"):
			v = False
		elif (response == "WAIT"):
			continue
		else:
			print "OPPONENT RAGE QUIT!! VOLVO PLS BAN!"
			quit()

		if (v):
			if (turn):
				kalah()
			else:
				menang()
		else:
			if (turn):
				menang()
			else:
				kalah()

		turn = not turn
		break

# main program starts here
if __name__ == "__main__":
	try:
		# check program arguments
		if len(sys.argv) != 3:
			print "Usage: python client.py <host> <port>"
			quit()

		# get server address
		HOST = sys.argv[1]
		PORT = int(sys.argv[2])

		# open connection to server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))

		# get turn from server
		global turn
		turn = getturn();

		while True:
			# if his turn, input
			if (turn):
				sendquest()
				getresult()

			# if his opp input, wait
			else:
				sendanswer()
				getresult()
				continue

			time.sleep(0.1)

	except KeyboardInterrupt:
		print('\nKeyboard interrupt detected. Exiting gracefully...\n')
		quit()
