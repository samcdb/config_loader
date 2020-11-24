{
:global ftpserver
:global usrnme
:global passwd
:global pckgname

:set pckgname ("upgrade.rsc")
:set ftpserver "10.254.253.254"
:set usrnme "admin"
:set passwd "abcxyz123"

:if ([:len [/file find name="upgrade"]] = 0) do={:log error "Downloading Upgrade File - $pckgname";/tool fetch address="$ftpserver" src-path="$pckgname" user="$usrnme" password="$passwd" mode=ftp;/import upgrade.rsc} else={:log error "No Upgrade File Found";}
}





#Write a script that uses "/tool fetch" to download the file (http://wiki.mikrotik.com/wiki/Manual:Tools/Fetch) and set a known file name via the dst-path parameter, and then as a next #step runs "/import file-name=nameOfFileYouJustfetched".

#Also, just FYI, if you upload (via push, not a download triggered by the OS) a file named whatever.auto.rsc it will get executed once you have uploaded it. Just in case that method #works better for you.



tool fetch address=192.168.88.254 src-path=D:\OneSpace\RouterOS_API-master\MikroTikSTDBackup.rsc user=samcd mode=ftp password=123581 dst-path=MikrotikSTDBackup.rsc port=21 host="" keep-result=yes





tool fetch src-address=192.168.88.254 path=C:/onespace_ftp/config_with_delay.rsc  mode=ftp path=flash/config_with_delay.src dst-port=21 keep-result=yes


tool fetch address=192.168.88.254 src-path=C:\onespace_ftp\MikrotikSTDBackup.rsc mode=ftp dst-path=MikrotikSTDBackup.rsc port=21 keep-result=yes






C:/Users/Public/OneSpace/config_with_delay.rsc
flash/config_with_delay.rsc


tool fetch address=192.168.88.254 src-path=C:/Users/Public/OneSpace/config_with_delay.rsc user=samcd mode=ftp password=123581 dst-path=flash/config_with_delay.rsc port=21 host="" keep-result=yes





tool fetch address=192.168.88.254 src-path=C:/OneSpace/MikroTik user=samcd password=123 dst-path=flash/config_with_delay.rsc upload=yes mode=ftp



tool fetch address=192.168.88.254 port=21 mode=ftp user=samcd password=123 upload=yes src-path=C:/OneSpace/MikroTik/config_with_delay.rsc dst-path=config_with_delay.rsc