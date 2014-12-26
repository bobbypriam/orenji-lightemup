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
# submit = ''

def getturn():
	response = s.recv(1024)
	if (response == "WAIT"):
		print "Too bad, you're second :)"
		return False
	elif (response == "NOW"):
		print "Whoo! You get to go first!"
		return True
	else:
		s.close()
		quit()

def is_valid(str):
	for c in str:
		if c.upper() not in ['K', 'M', 'H']:
			return False
	return True

def get_input():
	inp = raw_input("Can you light 'em up? (K, M, or H): ")
	while not is_valid(inp):
		print "Whoops, make sure it's one of K, M, or H!"
		inp = raw_input("Can you light 'em up? (K, M, or H): ")
	print
	return inp

def sendanswer():
	print "Please wait, the opponent is typing..."
	
	# global submit

	while True:
		s.send("AREDONE")
		response = s.recv(1024)
		if (response == "GO"):
			print
			print "You're good to go!"
			break
		time.sleep(0.5)

	answer = get_input()
	s.send(answer)
	print "Sent! Watch the lights..."
	# submit = answer
	time.sleep(0.5)

def sendquest():
	# global submit
	quest = get_input()
	s.send(quest)
	print "Sent! Watch the lights...\nPlease wait for your opponent's answer..."
	# submit = quest
	time.sleep(0.5)

def menang():
	print
	print "~~~~~~~~~~~~ Congratulations! You win! ~~~~~~~~~~~~"
	print

def kalah():
	print
	print "~~~~~~~~~~~~ Sorry, you lost! ~~~~~~~~~~~~"
	print

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

		# time.sleep(len(submit)+1)
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
		print "Now let's switch turns!"
		time.sleep(0.5)
		break

# main program starts here
if __name__ == "__main__":
	print """
=================================================
===                 Welcome to                ===
===        Light 'Em Up: The Memory Game!     ===
===                   (CLI)                   ===
===                                           ===
===             a game by ORENJI              ===
=================================================
	"""
	try:
		# open connection to server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))

		# get turn from server
		s.settimeout(0.5)
		turn = getturn();

		s.settimeout(None)
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
	except socket.error, msg:
		if msg[0] == 32:
			print "The server is reset, please connect again.\n"
		elif msg[0] == 111:
			print "Connection refused; is the server ready yet?\n"
		elif msg[0] == 'timed out':
			print "Whoops, maximum number of players reached!\n"
		else:
			print "Unhandled error: "
			print msg
