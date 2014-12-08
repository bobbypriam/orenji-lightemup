import socket
import sys
import json
import os
import time

HOST = ''
PORT = 8888

turn = True;

def getturn():
	# open connection to server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	response = s.recv(1024)
	if (response == "WAIT"):
		turn = False;
		print "Get Second turn ..."
	elif (response == "NOW"):
		turn = True;
		print "Get First turn ..."
	else:
		s.close()
		quit()

	s.close()

def sendanswer():
	# open connection to server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	while True:
		print "Waiting ..."

		s.send("AREDONE")
		response = s.recv(1024)

		if (response == "GO"):
			print "Now Answer!"
			break

	userinput = raw_input("Masukkan kombinasi warna K,M,H")
	s.send(userinput)

	s.close()

def sendquest():
	# open connection to server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	userinput = raw_input("Masukkan kombinasi warna K,M,H")
	s.send(userinput)

	s.close()

def menang():
	print "MUSUH ANDA COPO!"

def kalah():
	print "ANDA COPO!"

def getresult():
	# open connection to server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	while True:
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

	s.close()

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

		# get turn from server
		getturn();

		while True:
			# if his turn, input
			if (turn):
				sendquest()
				getresult()

			# if his opp input, wait
			else:
				sendanswer()
				getresult()

			time.sleep(0.1)

	except KeyboardInterrupt:
		print('\nKeyboard interrupt detected. Exiting gracefully...\n')
		quit()
