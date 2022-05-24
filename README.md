# piCorePhonie

I've been using the fantastic Phoniebox http://phoniebox.de/ for a couple of years, but Spotify just stopped working: https://github.com/MiczFlor/RPi-Jukebox-RFID/issues/1815

I have an LMS SqueezeboxServer server anyway that supports Spotify well, so I installed piCorePlayer https://www.picoreplayer.org/ to use my Phoniebox as an LMS SqueezeboxServer client and wrote a script based on  https://github.com/baztian/rfid-squeezectl to use RFID tags for starting Spotify playlists. This is not supposed to be a replacement for Phoniebox, just a quick and dirty fix to get Spotify working again quickly. 

See instructions below to set up a Phoniebox with control buttons, rotary encoder, rc522 RFID reader, status LEDs and an OnOff shim. Of course, there is no GUI and also an automatic shutdown when idling is missing. 

## Installation
Download picoreplayer https://docs.picoreplayer.org/downloads/ and follow instructions https://docs.picoreplayer.org/getting-started/ . Call player piCorePhonie



### Set up Wifi without Ethernet

Before inserting the SD card, add file wpa_supplicant.conf to boot partition:

    # Maintained by piCorePlayer
    ctrl_interface=/var/run/wpa_supplicant
    ctrl_interface_group=staff
    # Two Character Country Code
    country=US
    update_config=1

    network={
        ssid="yourssid"
        psk="password"
        key_mgmt=WPA-PSK
        auth_alg=OPEN
    }



### PCP Extensions:

Using the "main page" of the web GUI, resize the file system so that it uses the whole SD card ("resize FS"). Then, install these PCP extensions:
* python3.8-dev
* python3.8-pip
* python3.8-wheel
* python3.8-setuptools
* git
* gcc
* glibc_base_dev
* linux-5.10.y_api_headers
* pcp-sbpd



### backup python directory
**Important, do a backup using the pcioreplayer GUI before each reboot, otherwise changes are deleted!**

Make sure python directories are included in the backup. SSH to raspberry (https://docs.picoreplayer.org/how-to/access_pcp_via_ssh/) and run

    nano /opt/.filetool.list
to add

    usr/local/lib/python3.8/site-packages/


### RC522 rfid reader
Install python libraries
    sudo pip install squeezebox-controller pyyaml spidev RPi.GPIO

The pi-rc522 version on pypi didn't work for me, so take the github repo:

    cd /tmp
    git clone https://github.com/ondryaso/pi-rc522.git
    cd pi-rc522/
    sudo pip install .

Clone this repository
    git clone https://github.com/maahn/piCorePhonie


Create the config file /home/tc/rfid_config.yaml . Mine looks like

    host: 192.168.0.243
    port: 9000
    player: piCorePhonie
    80-243-128-154-185: "Spotify: weiss"
    115-232-255-127-27:  "Spotify: gelb"
    96-89-35-45-55: "Spotify: blau"
    134-20-108-241-15: "Spotify: grun"
    54-1-102-241-160: "Spotify: orange"

host port, and player name could be probably figured out automatically... The numbers are the ids of the RFID cards and the corresponding LMS playlists. 
To get the RFID ids, ssh to the raspberry, hold an RFID tag to the reader, and run
    
    python3 showRFID.py

Using the web GUI, got to tweaks, and add this picoreplayer User commands (under tweaks) to start the RFID
script after booting

    /home/tc/piCorePhonie/readRFID.py /home/tc/rfid_config.yaml > /home/tc/readRFID.out 2> /home/tc/readRFID.err


###  GPIO Buttons
sbpd is used for the GPIO buttons, see https://github.com/coolio107/SqueezeButtonPi-Daemon for details. 
See button.sh in the repository and modify th elast line. Make sure to check out https://abyz.me.uk/rpi/pigpio/faq.html#Sound_isnt_working for the t option of pigpiod and the script to the picoreplayer User commands under tweaks

    /home/tc/piCorePhonie/button.sh

### OnOff Shim
https://forums.slimdevices.com/showthread.php?109734-piCorePlayer-Pimoroni-OnOff-Shim

go to 'Tweaks' page of the PiCorePlayer GUI, under 'Poweroff/Shutdown Overlays'

- set gpio poweroff to 'yes' , '4', 'Active Low'
- set gpio shutdown to 'yes', '17', 'Active Low'
- click on 'Install Monitor'


### Startup sound
In case you want a startup sound, install extension pcp-mpg123 and copy a file to the user 
directory. Using the web GUI, got to tweaks, and add this user command 
    /usr/local/bin/mpg123 /home/tc/myfile.mp3

### Status LED
To add external status LEDs, follow https://docs.picoreplayer.org/how-to/edit_config_txt/ to edit config.txt

    dtoverlay=gpio-led,gpio=12,trigger=heartbeat,label=statusled0
    dtoverlay=gpio-led0,gpio=16,trigger=cpu,label=statusled1


### Store everything
Using the web GUI, don’t forget to do a backup, otherwise all changes are gone after a reboot
