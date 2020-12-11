#!/usr/bin/env bash

readonly SCRIPT="$(test -L "${BASH_SOURCE[0]}" && readlink "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")"
readonly SCRIPT_DIR="$(cd "$(dirname "${SCRIPT}")"; pwd)"
readonly RES_DIR="${SCRIPT_DIR}/examplefiles"

execute_script() {
    ### WLAN Interface
    echo "interface wlan0
        static ip_address=192.168.4.1/24
        nohook wpa_supplicant" >> /etc/dhcpcd.conf
    
    ### Routing
    # TODO: Don't append but just remove '#' in front of existing entry
    echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/routed-ap.conf

    ### iptables firewall
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo netfilter-persistent save

    ### DNS
    mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
    echo "interface=wlan0
    dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
    domain=wlan
    address=/gw.wlan/192.168.4.1" >> /etc/dnsmasq.conf

    ### Access Point 
    sudo systemctl unmask hostapd
    sudo systemctl enable hostapd
    mkdir -p "/etc/hostapd"
    cp "${RES_DIR}/hostapd.conf" "/etc/hostapd/hostapd.conf"

    ### Script in PATH
    cp "${SCRIPT_DIR}/changePassword.py" "/usr/local/bin/changePassword.py"
    cp "${SCRIPT_DIR}/buttonInput.py" "/usr/local/bin/buttonInput.py"

    ### Crontab
    echo "* 3 * * 1 root changePassword.py > /dev/tty1" >> "/etc/cron.d/changePassword"

    sudo reboot
}

# main
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
    echo "Script is being sourced"
else
    set -x
    set -euo pipefail
    execute_script "$@"
fi
