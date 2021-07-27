import subprocess
import optparse
import re
import os
from messages import banner


def get_input():
    usage = "python3 mac_changer.py -i eth0 (or your interface) -m 11:22:33:44:55:66 (or your choice)"
    parser_object = optparse.OptionParser(usage=usage)
    parser_object.add_option("-i", "--interface", dest="interface (wlan0, eth0, ...)", help="interface")
    parser_object.add_option("-m", "--mac", dest="mac_address", help="new mac address")
    # parser_object.add_option("-r", "--random", dest="random", help="random mac address")
    return parser_object.parse_args()


def change_mac_address(interface, mac_address):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def check_new_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    new_mac_address = re.search(r"..:..:..:..:..:..", str(ifconfig))
    if new_mac_address:
        return new_mac_address.group(0)


if os.getuid() != 0:
    print("You must be root")
else:
    banner()
    (options, arguments) = get_input()
    change_mac_address(options.interface, options.mac_address)
    new_mac = check_new_mac(options.interface)
    if new_mac == options.mac_address:
        print("Successfully Mac Address Changed!")
    else:
        print("Something went wrong")
