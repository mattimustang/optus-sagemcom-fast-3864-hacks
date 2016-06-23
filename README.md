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

However, thanks to some reverse engineering done by Matty123123 at the plus.net
forums there is a way to decrypt the configuration file obtained when you
download the backup settings from the router.

Open a web browser to `http://192.168.0.1` and navigate to Managment
/ Configuration / Backup and download the `backupsettings.conf` file.

Next download a copy the the decrypt-conf.py script included in this
repository.

Install the `decrypt-conf.py` dependencies:

    $ sudo pip install pycrypto

Decrypt the settings:

    $ python decrypt-conf.py backupsettings.conf

This will produce a new file called `backupsettings.conf.txt`. Search this file
for the lines:

          <AdminPassword>XXXXXXXXXXXXX==</AdminPassword>

The password is base64 encoded so to decode it copy it into the following
command line:

    $ echo XXXXXXXXXXXX== | base64 -d

To access the advanced menus enter the following URL with your routers password
into your browser:

    http://admin:xxxxx@192.168.0.1/main.html

Credit goes to Matt Goring for his original [Windows configuration decryption
tool](https://community.plus.net/t5/Tech-Help-Software-Hardware-etc/Unlocking-the-potential-of-Sagemcom-2704N/m-p/1223467#M64842) on which I based my python
script.

# Coming Soon...

- Uploading a modified configuration
- Enabling telnet
- Dumping the firmware
- Full list of URLs
- PSI configuration decoder

# References

- [Forum user Matty123123 has done quite a bit to reverse engineer the firmware
on a similar device](https://community.plus.net/t5/Tech-Help-Software-Hardware-etc/Unlocking-the-potential-of-Sagemcom-2704N/td-p/1223314) and [here](https://drive.google.com/folderview?id=0B4-Ln6UubyEeb1VQaTZDaXJzNVE)
-  [Help: Bundled modem Sagecom F@st 3864](http://forums.whirlpool.net.au/archive/2401743)
- [Optus NBN - router admin access, using a BYO router with VOIP](http://forums.whirlpool.net.au/archive/2238007)
- [Sagemcom F@ST 3864 V2 - Get Admin Password](https://www.exploit-db.com/exploits/37801/)
