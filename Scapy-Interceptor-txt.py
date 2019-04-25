#! /usr/bin/env python3
import subprocess
import tempfile
from netfilterqueue import NetfilterQueue
from scapy.all import *


### Config ###
#Editor to use (must be in path)
editor= "vim"

# Create a temporary file with the content and open the editor
def input_via_editor(editor, content=""):
	with tempfile.NamedTemporaryFile(mode='w') as temp_file:
		if content:
			temp_file.write(content)
			temp_file.flush()
		try:
			subprocess.check_call([editor, temp_file.name])
		except subprocess.CalledProcessError as e:
			raise IOError("{} exited with code {}.".format(editor, e.returncode))
		with open(temp_file.name) as temp_file_2:
			return temp_file_2.read()

# Proccess intercepted packets
def interrupt_and_edit(pkt):
	global editor
	
	packet = IP(pkt.get_payload())
	#packet = IP(pkt.get_payload()) #if want to edit the payload only
	
	#compute the equivalent scapy command
	scapy_command = packet.command()
	
	#let the user edit the scapy command
	user_defined_command = input_via_editor(editor, scapy_command)
	#convert to packet
	user_defined_packet = eval(user_defined_command)
        
	#force update of the checksum
	del user_defined_packet[IP].chksum
	#update the payload
	pkt.set_payload( raw(user_defined_packet) )
	
	#forward the packet
	pkt.accept()


if __name__=="__main__":

	nfqueue = NetfilterQueue()

	#Bind to the same queue number (here 2)
	nfqueue.bind(2, interrupt_and_edit)
	
	#run (indefinetely)
	try:
		nfqueue.run()
	except KeyboardInterrupt:
		print('Quiting...')
	nfqueue.unbind()
