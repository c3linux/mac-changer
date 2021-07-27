import subprocess
import optparse
import re


def get_input():
    parser_object = optparse.OptionParser()
    parser_object.add_option("-i", "--interface", dest="interface", help="interface")
    parser_object.add_option("-m", "--mac", dest="mac_address", help="new mac address")
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


(options, arguments) = get_input()
change_mac_address(options.interface, options.mac_address)
new_mac = check_new_mac(options.interface)
if new_mac == options.mac_address:
    print("Successfully Mac Address Changed!")
else:
    print("Something went wrong")
