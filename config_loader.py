from routeros_api import Api
import socket
import asyncio
import time
import tkinter

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



def main():
	
	reboot = '/system/reboot'
	fetch_file = '/tool/fetch =url=http://192.168.88.254:8000/config_with_delay.rsc =mode=http =dst-path=flash/config_with_delay.rsc'
	reset_config = '/system/reset-configuration =no-defaults=yes =run-after-reset=flash/config_with_delay.rsc'  

	while(True):
		try:
			
			router = Api('192.168.88.1')
			r = router.talk('/system/identity/print')
			print(r)
			print('connected')

					# router gets config file from web server
			router.talk(fetch_file)
			print("file fetched")
			router.talk(reset_config)
			print("resetting")
			time.sleep(3)

		except TimeOutError:
			print(timedout)
	#while(True):
	#	try:



	#	except Exception as inst:
	#		print(type(inst))

	#	finally:
	#		time.sleep(10)


if __name__ == "__main__":
    main()

















"""

user_input = input("Enter command:")

while (user_input != 'exit'):
	command = ""

	if (user_input == 'reset'):
		command = reset_config
	elif (user_input == 'reboot'):
		command = reboot
	elif (user_input == "change"):
		command = change_id
	elif (user_input == 'fetch'):
		command = fetch_file
	elif (user_input == 'run'):
		command = run_file
	else:
		print("Invalid command")

	if (len(command) > 0):
		response = router.talk(command)
		print(response)

	user_input = input("Enter command:")

"""



