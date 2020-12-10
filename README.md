# QRRaspAp

The QRRaspAP project was created as part of a university course. 
Our goal was to create a WLAN access point which automatically changes the passphrase every X days/weeks. Additionally a QRCode is displayed to connect to the network in a fast way. 
Usage could be for example as a guest network. 



## Prerequisites

On your raspberrypi you need all this:

```
sudo apt update 
sudo apt full-upgrade
sudo reboot
```

Install the necessary packages:

```
sudo apt-get install hostapd dnsmasq
sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent
sudo apt-get install python3 python3-pip
```

Install pip packages:

```
sudo pip3 install pyqrcode
sudo pip3 install gpiozero
```

## Getting Started




## License
[MIT](https://choosealicense.com/licenses/mit/)
