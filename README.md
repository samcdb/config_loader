
# Config Loader

Allows for the automatic installation of specified configuration files on multiple MikroTik routers

#### Features:

* Graphic User Interface for ease of use (robust features and guided user experience)
* Uses local web server for seamless file transfer
* Automatically iterates through all unconfigured routers connected to the computer (using network switch)

## RouterOS API

https://github.com/LaiArturs/RouterOS_API

This API was used to communicate with the MikroTik routers.


## Use

Config Loader allows an array of connected routers with default IP 192.168.88.1 (connected to a network switch along with the computer) to be iterated through, reset (with no default configuration)
and then configured with a chosen file (.rsc).

The user must set a static IP address of 192.168.88.(2-254) on their computer before running.
All requirements and necessary procedures are explained to the user via the GUI and any invalid entries or commands are blocked.

### PLEASE NOTE!
the RouterOS/MikroTik 'Run After Reset' function does not work properly. The script needs to wait 15s before running. This means that any .rsc files that are selected that do not 
start with a 15s delay will be copied and a temporary version with a delay will be written. This copy will be run by Config Loader and subsequently deleted.


The line below is written at the beginning of the script:

	:delay 15s;















