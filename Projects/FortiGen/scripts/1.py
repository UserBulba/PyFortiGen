from ipaddress import IPv4Interface, IPv4Network
device = "10.149.160.1"
ifc = IPv4Interface(device + "/28")

print(ifc.ip)  # The host IP address
print(ifc.network)  # Network in which the host IP resides
