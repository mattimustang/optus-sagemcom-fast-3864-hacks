
# Overview

This repository is a collection of tools and tips for the Optus Sagemcom
F@ST 3864 broadband modem.

## NOTE: Optus has patched out the ability to upload unencrypted configuration files, so the only way to upload them is if you re-encrypt them. Apparently the IV and the Key has also changed, which means that the decryption tool now doesn't work on newer firmwares.

# Getting Access to Advanced Configuration Options

The advanced features of the modem are not accessible by default and require
you to login as the `admin` user to be able to view and modify them.

There are a number of ways you can obtain the admin password, with some methods
depending on the firmware version your modem is running.

# Known Working Firmware Versions

The techniques below only work with certain firmware versions. Browse to http://192.168.0.1/main.html?loginuser=1 and check the `Software Version` against the table below to see if it is supported. To get access for devices with unsupported firmware I will required a device running that firmware or someone to investigate and provide a fix for their firmware version. 

| Software Version | Supported |
| --- | --- |
| before 8.353.1_F@ST5350_Optus | Yes |
| 8.353.1_F@ST5350_Optus | Yes |
| 8.353.21_F@ST5350_OptusBootloader | No |
| 8.379_F@ST3864AC_Optus | No |
| 10.33_F@ST3864V3AC_Optus | No |
| 10.54_F@ST3864V3AC_Optus | No |


## Factory Default Passwords

Listed below are the factory default passwords set on Optus' devices.
These get automatically changed from the defaults when you connect the device to the Internet for the first time.

Leave the modem WAN/DSL ports disconnected if you want to access the modem using these passwords.

Stick a paperclip in the `RESET` button for 5 seconds to reset the modem to factory default configuration.

The passwords differ between modem models and firmware verions so try each one below until it works.

| user | password | url | status |
| --- | --- | --- | --- |
| admin | Y3s0ptus | http://admin:Y3s0ptus@192.168.0.1/main.html | Old patched out password. |
| admin | 0ptU%1M5 |  http://admin:0ptU%1M5@192.168.0.1/main.html | untested |
| admin | 8PTu5W@C | http://admin:8PTu5W%40C@192.168.0.1/main.html | CONFIRMED WORKING ON LATEST F@ST 3864v1 FIRMWARE|

## Getting the `admin` Password Prior to Software Version 8.353.1_F@ST5350_Optus

Getting the `admin` user password prior to firmware version 
`8.353.1_F@ST5350_Optus` such as version `7.253.2_F3864V2_Optus`.

Open a web browser to `http://192.168.0.1` and navigate to Managment / Access
Control and view the source of the righthand part of the page. Near the top of
the page you will find a line something like this:

    pwdAdmin = "XXXXXXX";

This is the `admin` user password.

If you now open your browser to `http://192.168.0.1/main.html?loginuser=0` and
enter the `admin` user and password details found you will enable the advanced
configuration menus.

## Getting the `admin` Password All Versions

From firmware version `8.353.1_F@ST5350_Optus` access to the advanced settings
was disabled, as was the ability to view the `admin` password in the Access
Control page.

However, thanks to some reverse engineering done by `Matty123123` at the `plus.net`
forums there is a way to decrypt the configuration file obtained when you
download the backup settings from the router.

Open a web browser to `http://192.168.0.1` and navigate to Managment
/ Configuration / Backup and download the `backupsettings.conf` file.

Next download a copy the the decrypt-conf.py script included in this
repository.

NOTE: If you already have the admin password, you can dump the config through this script: http://192.168.0.1/dumpcfgdynamic.cmd 
### Set up Linux
Install pip if you haven't already:

    $ sudo apt install python3-pip
    
Install the `decrypt-conf.py` dependencies:

    $ sudo pip install pycryptodome

### Set up Windows

On Windows systems will need to download and install [python 3.5](https://www.python.org/downloads/). Make sure you check the box to add Python to your PATH in the installer.

Then open a DOS or PowerShell command shell and install the pycrypto module:

    pip install pycryptodome

### Download `decrypt-conf.py`

Download the 
[`decrypt-conf.py`](https://raw.githubusercontent.com/mattimustang/optus-sagemcom-fast-3864-hacks/master/decrypt-conf.py) script and you `backupsettings.conf` from your modem and put them in the same directory.


### Decrypt the Settings

On Linux/Unix-like systems run:

    $ python decrypt-conf.py backupsettings.conf

or on Windwos:

    > python.exe decrypt-conf.py backupsettings.conf

This will produce a new file called `backupsettings.conf.txt`. Search this file
for the lines:

          <AdminPassword>XXXXXXXXXXXXX==</AdminPassword>

The password is base64 encoded so to decode it copy it into the following
command line:

    $ echo XXXXXXXXXXXX== | base64 -d

## Accessing the Advanced Settings

To access the advanced menus enter the following URL with your router's `admin` password
into your browser:

    http://admin:xxxxx@192.168.0.1/main.html

Credit goes to Matt Goring for his original [Windows configuration decryption
tool](https://community.plus.net/t5/Tech-Help-Software-Hardware-etc/Unlocking-the-potential-of-Sagemcom-2704N/m-p/1223467#M64842) on which I based my python
script.

# Uploading a Modified Configuration

Once you have obtained a plain text version of the configuration you can then
modify it and upload it to the device.

Open a web browser to `http://192.168.0.1` and navigate to Managment
/ Configuration / Update and upload your modified the `backupsettings.conf.txt` file.

There is no need to encrypt the file as the router will accept plain text files.

# Enabling Telnet

Enabling telnet allows you to explore the device a little more and customize it
further from the Linux command line.

To enable telnet you need to modify a plain text copy of the configuration to
include the line:

    <X_GVT_Telnet_Enable>TRUE</X_GVT_Telnet_Enable>

The configuration may already contain the line above but it is set to `FALSE` so
just change it to `TRUE`.

If it is missing the line then add it after the following line:

    <InternetGatewayDevice>

Then upload the modified configuration.

You will now be able to telnet to `192.168.0.1` and login using the username
`admin` and the password you obtained earlier. Once you are logged in you are
put into a restricted shell so type `sh` to drop into a BusyBox Linux shell.

# Putting the device into bridge mode

## ADSL2 Connections

Follow the instructions in the PDF to [put Optus F@st 3864 modem into bridge mode](brigesagemcom3864.pdf). Original credit to [Ray Haverfield](https://sites.google.com/site/lapastenague).

Note:
- Use the instructions above to obtain your admin password rather than those in the PDF.

## NBN FTTN/VDSL Connections

The NDN FTTN/VDSL steps are similar to ADSL:

1. Backup your existing configuration in case you want to revert to it later.
2. Factory reset the modem by hold a paper clip in the reset hole at the back of the modem until all the lights flash and it reboots.
3. Use the instructions above to obtain your admin password.
4. Open a web browser to [http://192.168.0.1/main.html](http://192.168.0.1/main.html) and login as admin with the password obtained in the previous step.
5. Navigate to `Advanced Setup / WAN Service`. Look for the row in the table with interface `ptm0.1` and description `ipoe_0_1_1.0`. Select the `Remove` checkbox for that row only and click the `Remove` button. This will remove the non-bridged NBN FTTN VDSL WAN interface.
7. Navigate to `Advanced Setup / WAN Service` and click the `Add` button. This will start a wizard-like set of forms for configuring the WAN Service Interface.
8. On the first page select a layer 2 interface for the service. Select `ptm0/(0_1_1)` and click `Next`.
9. On the next page select the WAN service type `Bridging`. Do not change any other settings. Click `Next`.
10. On the next page is a summary of the settings. Click `Apply/Save`.
11. Next you will need to disable DHCP on the modem so that the alternative routing device you are bridging can get a public IP via DHCP. Navigate to `Advanced Setup / LAN` and select `Disable DHCP Server` and click `Apply/Save`.
12. Next you should disable wireless. Navigate to `Wireless` and uncheck the `Enable Wireless` box. Click `Apply/Save`.
13. Then reboot the modem by clicking the reboot button in the status widget at the top right.

Once the modem has rebooted and the VDSL connection is established you can connect your other router's ethernet WAN interface into the Optus modem. Configure your other router to use DHCP on the WAN interface and it should get an IP address handed out to it from upstream server at Optus. If you get a 192.168.0.x IP address then you haven't disabled DHCP on the Optus F@st 3864 modem and you'll need to connect a PC to it again to do that.

Note: Once you have disabled DHCP on the F@st 3864, if you ever need to make changes to it you will need to connect a computer to it with an ethernet cable and manually configure and IP address on your computer. Use 192.168.0.2 or higher. Then you will be able to browse to http://192.168.0.1 to make changes.

Note: You can test if bridging is working by plugging a computer using an ethernet cable and having DHCP configured. However, **I strongly discourage doing this unless you know what you are doing and are sure that your computer's operating system is 100% up to date with all operating system security patches. Your computer will not have time to check for patches and update before you will be scanned and hacked within minutes. You have been warned!**

# Coming Soon...

- Dumping the firmware
- Full list of URLs
- PSI configuration decoder

# References

- [Forum user Matty123123 has done quite a bit to reverse engineer the firmware
on a similar device](https://community.plus.net/t5/Tech-Help-Software-Hardware-etc/Unlocking-the-potential-of-Sagemcom-2704N/td-p/1223314) and [here](https://drive.google.com/folderview?id=0B4-Ln6UubyEeb1VQaTZDaXJzNVE)
-  [Help: Bundled modem Sagecom F@st 3864](http://forums.whirlpool.net.au/archive/2401743)
- [Optus NBN - router admin access, using a BYO router with VOIP](http://forums.whirlpool.net.au/archive/2238007)
- [Sagemcom F@ST 3864 V2 - Get Admin Password](https://www.exploit-db.com/exploits/37801/)
- [Frank's Hacks](http://frankhacks.blogspot.com.au/2016/03/fst3864.html)
- [Thank's to Paul 88888 on Whirlpool for finding the dumpcfgdynamic.cmd to view config without decrypting every time.](https://whrl.pl/ReiHOn)
