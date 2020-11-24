# jan/02/1970 02:06:53 by RouterOS 6.45.8
# software id = RN41-ZVE2
#
# model = RBwAPR-2nD
# serial number = AE850C68C0CE
:delay 15s;
/interface bridge
add admin-mac=48:8F:5A:68:B2:04 auto-mac=no comment=defconf name=bridge
/interface list
add comment=defconf name=WAN
add comment=defconf name=LAN
/interface lte apn
add apn=unrestricted default-route-distance=1
/interface lte
set [ find ] allow-roaming=yes apn-profiles=unrestricted mac-address=\
    AC:FF:FF:00:00:00 name=lte1
/interface wireless security-profiles
set [ find default=yes ] supplicant-identity=MikroTik
add authentication-types=wpa2-psk eap-methods="" management-protection=\
    allowed mode=dynamic-keys name=Tech5WIFIKey supplicant-identity="" \
    wpa2-pre-shared-key=Letmein321
/interface wireless
set [ find default-name=wlan1 ] band=2ghz-onlyn channel-width=20/40mhz-Ce \
    country="south africa" disabled=no distance=indoors installation=outdoor \
    mode=ap-bridge security-profile=Tech5WIFIKey ssid=SnipR-Wifi \
    wireless-protocol=802.11
/ip pool
add name=default-dhcp ranges=192.168.88.10-192.168.88.254
add name=dhcp ranges=192.168.1.200-192.168.1.254
/ip dhcp-server
add address-pool=dhcp disabled=no interface=bridge name=dhcp1
/interface bridge port
add bridge=bridge comment=defconf interface=ether1
add bridge=bridge comment=defconf interface=wlan1
/ip neighbor discovery-settings
set discover-interface-list=LAN
/interface list member
add comment=defconf interface=bridge list=LAN
add comment=defconf interface=lte1 list=WAN
/ip address
add address=192.168.1.1/24 interface=bridge network=192.168.1.0
/ip cloud
set ddns-enabled=yes
/ip dhcp-server network
add address=192.168.1.0/24 gateway=192.168.1.1
add address=192.168.88.0/24 comment=defconf gateway=192.168.88.1
/ip dns
set allow-remote-requests=yes servers=1.1.1.1
/ip dns static
add address=192.168.88.1 comment=defconf name=router.lan
add address=192.168.1.1 name=lte
/ip firewall address-list
add address=41.78.245.200 list=Tech5
add address=41.78.245.204 list=Tech5
add address=41.78.245.20 list=Tech5
add address=165.255.254.3 list=Tech5
add address=41.0.147.70 list=Tech5
add address=169.239.180.250 list=Tech5
add address=41.78.244.44 list=Tech5
add address=197.0.0.0/8 list=Local
add address=165.0.0.0/8 list=Local
add address=196.0.0.0/8 list=Local
add address=41.0.0.0/8 list=Local
add address=105.0.0.0/8 list=Local
add address=192.0.0.0/8 list=Local
add address=154.118.244.226 list=Local
/ip firewall filter
add action=accept chain=input in-interface=lte1 src-address=196.0.0.0/8
add action=accept chain=input in-interface=lte1 src-address=41.78.0.0/16
add chain=input comment=Basic protocol=icmp
add chain=input connection-state=established,related
add chain=forward connection-state=established,related
add action=drop chain=forward connection-state=invalid
add chain=input comment=Tech5 src-address=41.78.245.200
add chain=input src-address=41.78.245.204
add chain=input src-address=41.78.245.20
add chain=input src-address=165.255.254.3
add chain=input src-address=41.0.147.70
add chain=input src-address=169.239.180.250
add action=drop chain=input comment="Drop all Lte" in-interface=lte1
add action=drop chain=forward comment="Drop all not NAT" \
    connection-nat-state=!dstnat connection-state=new in-interface=lte1
/ip firewall nat
add action=masquerade chain=srcnat comment="defconf: masquerade" \
    ipsec-policy=out,none out-interface=lte1 out-interface-list=WAN
add action=dst-nat chain=dstnat dst-port=2222 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.100 to-ports=22
add action=dst-nat chain=dstnat dst-port=3333 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.250 to-ports=22
add action=dst-nat chain=dstnat dst-port=8181 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.100 to-ports=8080
add action=dst-nat chain=dstnat dst-port=8282 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.101 to-ports=80
add action=dst-nat chain=dstnat dst-port=9292 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.101 to-ports=22
add action=dst-nat chain=dstnat dst-port=8001 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.101 to-ports=8000
add action=dst-nat chain=dstnat dst-port=8383 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.102 to-ports=80
add action=dst-nat chain=dstnat dst-port=9393 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.102 to-ports=22
add action=dst-nat chain=dstnat dst-port=8002 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.102 to-ports=8000
add action=dst-nat chain=dstnat dst-port=8484 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.103 to-ports=80
add action=dst-nat chain=dstnat dst-port=9494 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.103 to-ports=22
add action=dst-nat chain=dstnat dst-port=8003 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.103 to-ports=8000
add action=dst-nat chain=dstnat dst-port=8585 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.104 to-ports=80
add action=dst-nat chain=dstnat dst-port=9595 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.104 to-ports=22
add action=dst-nat chain=dstnat dst-port=8004 in-interface=lte1 protocol=tcp \
    to-addresses=192.168.1.104 to-ports=8000
/ip service
set telnet disabled=yes
set ftp disabled=yes
set ssh disabled=yes
/system clock
set time-zone-name=Africa/Johannesburg
/system identity
set name="Snipr LTE"
/system script
add dont-require-permissions=yes name=NetWatchBoot-8.8.8.8 owner=admin \
    policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon \
    source=":local addresstoping 8.8.8.8;\r\
    \n:local interface \"lte1\";\r\
    \n:local continue true;\r\
    \n:local counter 0;\r\
    \n:local maxcounter 19;\r\
    \n:local sleepseconds 10;\r\
    \n:local goodpings 0;\r\
    \n:log error \"-----> Warwick's Netwatch-Script-Warning - Netwatch could n\
    ot ping \$addresstoping - Will begin further testing in \$sleepseconds sec\
    onds - and will continue for \$maxcounter times \$sleepseconds seconds\";\
    \r\
    \n:while (\$continue) do={\r\
    \n:set counter (\$counter + 1);\r\
    \n:delay \$sleepseconds;\r\
    \n:if ([/ping \$addresstoping interval=1 count=1] =0) do={\r\
    \n:log info \"----->ping to \$addresstoping failed on attempt \$counter of\
    \_\$maxcounter -- Will try again in \$sleepseconds seconds\";\r\
    \n} else {\r\
    \n:if ([:pick [:pick [/tool netwatch print detail as-value] 0] 6] = \"up\"\
    ) do={\r\
    \n:log warning \"-----> ping success on to \$addresstoping attempt \$count\
    er of \$maxcounter <----- Netwatch is Up --- Program will exit -----\";\r\
    \n:set continue false;\r\
    \n:set goodpings (\$goodpings +1);\r\
    \n} else {\r\
    \n:log warning \"-----> ping success on to \$addresstoping attempt \$count\
    er of \$maxcounter <----- Netwatch is Down --- Program will try again in \
    \$sleepseconds seconds -----\";\r\
    \n}\r\
    \n};\r\
    \n\r\
    \n:if (\$counter>=\$maxcounter) do={:set continue false;}\r\
    \n} \r\
    \n\r\
    \n:if (\$\"goodpings\" = 0 ) do={\r\
    \n:log info \"-----> Rebooting in 15 seconds\";\r\
    \n:delay 5;\r\
    \n:log error \"-----> Rebooting in 10 seconds\";\r\
    \n:delay 5;\r\
    \n:log error \"-----> Rebooting in 5 seconds\";\r\
    \n:delay 5;\r\
    \n:log error \"-----> Rebooting now\";\r\
    \n:delay 1;\r\
    \n/system reboot\r\
    \n/system reboot\r\
    \n/system reboot\r\
    \n/system reboot\r\
    \n}"
/tool mac-server
set allowed-interface-list=LAN
/tool mac-server mac-winbox
set allowed-interface-list=LAN
/tool netwatch
add down-script="log info \"Netwatch missed a ping to 8.8.8.8 - starting timeo\
    ut auto reboot script\" ; /system script run NetWatchBoot-8.8.8.8" host=\
    8.8.8.8
