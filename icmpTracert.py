 # Program to implement the traceroute in Python.
 # Usages : sudo python txtraceroute.py -m 20 www.google.com
 # Usages : sudo python icmpTracert.py  -p icmp -g www.google.com
 
 
from socket import *
import struct 
import sys
import random
import time
import json
import urllib
import os
import getopt

from twisted.python import usage

ICMP_ECHO_REQUEST = 8

'''
 * Input : Ip address
 * Return : Geographic location of the ip address, in terms of Country Name,Region Name,City 
 '''

def geoip_lookup(ip):
    try:
        address = "http://freegeoip.net/json/"+ip
        r = urllib.urlopen(address).read()
        # r = getPage("http://freegeoip.net/json/%s" % ip)
        d = json.loads(r)
        items = [d["country_name"], d["region_name"], d["city"]]
        text = ", ".join([s for s in items if s])
        text = text.encode("utf-8")
        return text
    except Exception:
        return ""

'''
 * Input : Data inside the packet
 * Return : Calculates the checksum and retuns the checksum 
 '''
def checksum(source_string):
    """ Calculates the checksum of the data 
        inside your packet 
    """
    checksum = 0
    count_to = len(source_string) & -2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1]) * 256 + ord(source_string[count])
        checksum += this_val
        checksum &= 0xffffffff 
        count += 2
    if count_to < len(source_string):
        checksum += ord(source_string[len(source_string) - 1])
        checksum &= 0xffffffff  
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += checksum >> 16
    answer = ~checksum
    answer &= 0xffff
    return answer >> 8 | (answer << 8 & 0xff00)

'''
 * Input : Takes the input id of the packet
 * Return : The packets after adding the Header and the Data together
 '''
def create_packet(id):
    """Creates a new echo request packet based on the given "id"."""
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = 192 * "Q"

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, htons(checksum(header + data)), id, 1)
    return header + data

def main(dest_name,  domain_name, **settings):
    
    dest_addr = dest_name
    # print dest_addr
    port = settings.get("dport")                #port on which we receive packets
    port = int(port)
    max_hops = settings.get("max_hops")
    max_hops = int(max_hops)
    time_out = settings.get("timeout")
    time_out = float(time_out)
    icmp = getprotobyname('icmp')
    udp = getprotobyname('udp')
    ttl = 1                                     #start with TTL of 1

    print "\nTracing route to %s [%s] \nover a maximum of %s hops: \n" % (domain_name,dest_addr,max_hops)   

    while True:
        print '{:>2}   '.format(ttl),

        #create 2 sockets, both raw, one to receive, one to send
        if settings.get("proto") == "icmp":
            recv_socket = socket(AF_INET, SOCK_RAW, icmp)
            send_socket = socket(AF_INET, SOCK_RAW, icmp)
        elif settings.get("proto") == "udp":
            recv_socket = socket(AF_INET, SOCK_RAW, icmp)
            send_socket = socket(AF_INET, SOCK_DGRAM, udp)
        # elif settings.get("proto") == "tcp":
        #     recv_socket = socket(AF_INET, SOCK_RAW, icmp)
        #     send_socket = socket(AF_INET, SOCK_STREAM,0)
        else:
            pass                
        # else:      
        #set value of ttl for the packet
        send_socket.setsockopt(SOL_IP, IP_TTL, ttl)
        
        # after this much time, we stop waiting for response
        # max_timeout = struct.pack("ll", 3, 0)
        max_timeout = struct.pack("ll",time_out,0)
        # print time_out
        # max_timeout = time_out
        # Set the receive timeout so we behave more like regular traceroute
        
        recv_socket.setsockopt(SOL_SOCKET, SO_RCVTIMEO, max_timeout)
        #bind socket to port
        recv_socket.bind(("", port))        
        curr_addr = None
        curr_name = None
        finished = False

        notAvail = 0;
        #stores RTT for multiple packets on the same hop
        dt = []
        #number of tries
        tries = settings.get("max_tries")
        #runs loop (max number of packets to send to one host)
        while tries > 0:
            #create packet_id, and then create packet
            packet_id = int(random.random() % 65535)
            packet = create_packet(packet_id)

            #send packet, the host as its destination
            send_socket.sendto(packet, (dest_name,1))   

            #start timer (to calculate RTT)         
            start = time.time()
            
            while True:
                #try receiving packet
                #if timeout occurs, exception is raised
                #which is caught
                try:                    
                    _, curr_addr = recv_socket.recvfrom(512)
                    
                    #append RTT to RTT list
                    dt.append(str(int((time.time() - start) * 1000)) + " ms")
                    #extract address
                    curr_addr = curr_addr[0]
                    
                    # print curr_addr
                    #extract host name, if there is one
                    try:
                        curr_name = gethostbyaddr(curr_addr)[0]
                    except error:
                        curr_name = curr_addr
                    break

                #if packet receive timesout    
                except error as (errno, errmsg):
                    dt.append("  *   ")
                    notAvail = 1
                    break
            #number of retries decreases
            tries = tries - 1
        # geoip_lookup(curr_addr)
        #close sockets
        send_socket.close()
        recv_socket.close()
        # print port
        if not finished:
            pass
        
        #if addr exists
        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = ""

        #lots of formatting            

        outxx = ""
        for i in dt:
            outxx = outxx + "{:>7}   "
        abcd = "{:<40}"
        xx = outxx.format(*dt)
        # location = geoip_lookup(curr_addr)
        # geoip_value = settings.get("geoip_lookup")
        # print settings.get("geoip_lookup")
        if settings.get("geoip_lookup") == False:
            print xx + abcd.format(curr_host)
        elif settings.get("reverse_lookup") == False:
            if curr_addr == None :
                print xx
            else:
                print xx + abcd.format(curr_addr)   
        else:    
            print xx + abcd.format(curr_host) + geoip_lookup(curr_addr)        

        #increase ttl
        ttl += 1
        # print 'max_hops =' + max_hops + 'ttl =' + str(ttl)
        #if destination reached, or max_hops exceeded,
        #we end the loop
        if (ttl > max_hops):
            print("MAX_HOPS LIMIT EXCEEDED.")
            break

        elif curr_addr == dest_addr:
                break

'''
 * Options Class : This will allow us to take several input combinations from the user.
 * This class automatically takes care of automatic combinations of the options possible.
'''

class Options(usage.Options):
    optFlags = [
        ["no-dns", "n", "Show numeric IPs only, not their host names."],
        ["no-geoip", "g", "Do not collect and show GeoIP information"],        
        ["help", "h", "Show this help"],
    ]
    optParameters = [
        ["timeout", "t", 2, "Timeout for probe packets"],
        ["tries", "r", 3, "How many tries before give up probing a hop"],
        ["proto", "p", "icmp", "What protocol to use (tcp, udp, icmp)"],        
        ["max_hops", "m", 30, "Max number of hops to probe"],        
    ]

'''
 * __name__ : Describes the vaious options in which you can take the input from User.
 * defaults : Default input value is chosen for the program execution.
 * @ return : Reports Error and exit, Otherwise call the main() with the respective input.
  
 '''

if __name__ == "__main__":
    defaults = dict(reverse_lookup=True,
                    geoip_lookup=True,
                    timeout=2,
                    proto="icmp",
                    dport = 123,
                    # dport=random.randint(2 ** 10, 2 ** 16),
                    # sport=random.randint(2 ** 10, 2 ** 16),
                    sport = 123,
                    max_tries=3,
                    max_hops=30)

    if len(sys.argv) < 2:
        print("Usage: %s [options] host" % (sys.argv[0]))
        print("%s: Try --help for usage details." % (sys.argv[0]))
        sys.exit(1)

    target = sys.argv.pop(-1) if sys.argv[-1][0] != "-" else ""
    domain_name = target    
    config = Options()
    try:
        config.parseOptions()
        if not target:
            raise
    except usage.UsageError, e:
        print("%s: %s" % (sys.argv[0], e))
        print("%s: Try --help for usage details." % (sys.argv[0]))
        sys.exit(1)

    settings = defaults.copy()
    if config.get("no-dns"):
        settings["reverse_lookup"] = False
    if config.get("no-geoip"):
        settings["geoip_lookup"] = False
    if "timeout" in config:
        settings["timeout"] = config["timeout"]
    if "tries" in config:
        settings["max_tries"] = int(config["tries"])
    if "proto" in config:
        settings["proto"] = config["proto"]
    if "max_hops" in config:
        settings["max_hops"] = config["max_hops"]
    if "dport" in config:
        settings["dport"] = int(config["dport"])
    if "sport" in config:
         settings["sport"] = int(config["sport"])
    
    if os.getuid() != 0:
        print("traceroute needs root privileges for the raw socket")
        sys.exit(1)
    try:
        target = gethostbyname(target)
    except Exception, e:
        print("could not resolve '%s': %s" % (target, str(e)))
        sys.exit(1)       

    main(target,domain_name,**settings) #call to the main function
