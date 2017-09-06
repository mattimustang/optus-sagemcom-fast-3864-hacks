# Overview

This repository is a collection of tools and tips for the Optus Sagemcom
F@ST 3864 broadband modem.

# Getting Access to Advanced Configuration Options

The advanced features of the modem are not accessible by default and require
you to login as the `admin` user to be able to view and modify them.

There are a number of ways you can obtain the admin password, with some methods
depending on the firmware version your modem is running.

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

### Set up Linux

Install the `decrypt-conf.py` dependencies:

    $ sudo pip install pycrypto

### Set up Windows

On Windows systems will need to download and install [python 3.5](https://www.python.org/downloads/). Make sure you check the box to add Python to your PATH in the installer.

Then open a DOS or PowerShell command shell and install the pycrypto module:

    pip install --use-wheel --no-index --find-links=https://github.com/sfbahr/PyCrypto-Wheels/raw/master/pycrypto-2.6.1-cp35-none-win32.whl pycrypto

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

Follow the instructions in the PDF to [put Optus F@st 3864 modem into bridge mode](brigesagemcom3864.pdf). Original credit to [Ray Haverfield](https://sites.google.com/site/lapastenague).

Note:
- Use the instructions above to obtain your admin password rather than those in the PDF.
- The configuration instructions are for ADSL2 connections, not NBN VDSL connetions, and will need to be updated when I get NBN in about a month. I suspect the difference will be instead of removing interface `ppp2. Internet-ADSL` you will need to remove the interface `ppp1.1 Internet-NBN`.

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
