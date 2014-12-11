import socket
import sys
import json
import os
import time

HOST = '192.168.42.1'
# HOST = 'localhost'
PORT = 10000

turn = True;

s = None

def getturn():
	response = s.recv(1024)
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
	print "Waiting for other player..."
	while True:

		s.send("AREDONE")
		response = s.recv(1024)

		if (response == "GO"):
			print "Now Answer!"
			break

		time.sleep(0.5)

	userinput = raw_input("Masukkan kombinasi jawaban warna K,M,H: ")
	s.send(userinput)
	time.sleep(0.5)

def sendquest():
	userinput = raw_input("Masukkan kombinasi warna K,M,H: ")
	s.send(userinput)
	time.sleep(0.5)

def menang():
	print "Selamat, Anda menang!"

def kalah():
	print "Maaf, Anda kalah!"

def getresult():
	global turn
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
		time.sleep(0.5)
		break

# main program starts here
if __name__ == "__main__":
	try:
		# open connection to server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))

		# get turn from server
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
