# Traceroute in Python

### Synopsis
----
Traceroute records the route through the Internet between your computer and a specified destination computer. It also calculates and displays the amount of time taken in getting the response from each Hop till we reach the destination.
Traceroute is a handy tool both for understanding where problems are in the Internet network and for getting a detailed sense of the Internet itself.

### Tech Details
----
When you execute the program, the program initiates the sending of a packet (using the Internet Control Message Protocol or ICMP), including in the packet a time limit value (known as the "time to live" (TTL) that is designed to be exceeded by the first router that receives it, which will return a Time Exceeded message. 
This enables traceroute to determine the time required for the hop to the first router. Increasing the time limit value, it resends the packet so that it will reach the second router in the path to the destination, which returns another Time Exceeded message, and so forth. 
Traceroute determines when the packet has reached the destination by matching the destination IP address against the last Hop returned IP address.
As the tracerouting progresses, the records are displayed for you hop by hop. Actually, each hop is measured three times. (If you see an asterisk (*), this indicates a hop that exceeded some limit.)

Note:- (*) does not indicate that the network is down. It may be the case the router is too busy to handle the network traffic and therefore discarded the packet.

### How does it work?
---
We send a ICMP packet with increasing TTL until we reach our destination

### Getting Started
---
Please verify that you have the below configuration installed in your system, before trying to execute the code.

Softwares Used:
  - Install Python Version 2.x
  - Ubuntu Operating System

Libraries Used:
 - "twisted" licensed by MIT
 - json

### Setup
---
General:- 
sudo python icmpTracert.py <ipaddress/DomainName>
E.g.

```sh
$ sudo python icmpTracert.py www.google.com
```
Options:
```
  -n, --no-dns,     Show numeric IPs only, not their host names
  -g, --no-geoip,   Do not collect and show GeoIP information
  -t, --timeout,    Timeout for probe packets [default: 2]
  -r, --tries,      How many tries before give up probing a hop [default: 3]
  -p, --proto,      What protocol to use (tcp, udp, icmp) [default: icmp]
  -m, --max_hops,   Max number of hops to probe [default: 30]
  -h, --help,       Display this help and exit
```
E.g.

```sh
$ sudo python icmpTracert.py -n www.google.com
$ sudo python icmpTracert.py -g www.google.com
$ sudo python icmpTracert.py -t 2 www.google.com
$ sudo python icmpTracert.py -r 5 www.google.com
$ sudo python icmpTracert.py -p icmp www.google.com
$ sudo python icmpTracert.py -m 30 icmp www.google.com
```
You may also use the combinations of two options.

E.g.

```sh
$ sudo python icmpTracert.py -n -t 2 www.google.com
$ sudo python icmpTracert.py -n -m 30 www.google.com
$ sudo python icmpTracert.py -g -m 30 www.google.com
```
### Demo Results
---
Eg. 

```sh
$ sudo python icmpTracert.py www.google.com
```
```
Tracing route to www.google.com [74.125.200.105] 
over a maximum of 30 hops: 

 1       3 ms      5 ms      9 ms   172.16.0.3 (172.16.0.3)                 
 2       7 ms      3 ms      6 ms   192.168.8.3 (192.168.8.3)               
 3       2 ms      3 ms      3 ms   F7001.iith.ac.in (192.168.8.8)          
 4      14 ms      1 ms      2 ms   218.248.6.129 (218.248.6.129)           India, Telangana, Medak
 5       5 ms      6 ms      6 ms   210.212.69.38 (210.212.69.38)           India, National Capital Territory of Delhi, New Delhi
 6      19 ms     19 ms     21 ms   218.248.178.42 (218.248.178.42)         India, Uttar Pradesh, Noida
 7      23 ms     20 ms     24 ms   72.14.211.114 (72.14.211.114)           United States, California, Mountain View
 8      19 ms     19 ms     31 ms   72.14.233.204 (72.14.233.204)           United States, California, Mountain View
 9      54 ms     54 ms     50 ms   72.14.238.178 (72.14.238.178)           United States, California, Mountain View
10      75 ms     66 ms     54 ms   72.14.239.61 (72.14.239.61)             United States, California, Mountain View
11       *         *         *                                              
12       *         *         *                                              
13       *         *         *                                              
14       *         *         *                                              
15       *         *         *                                              
16       *         *         *                                              
17       *         *         *                                              
18       *         *         *                                              
19      56 ms     54 ms     54 ms   sa-in-f105.1e100.net (74.125.200.105)   United States, California, Mountain View
```
### References
---
Ksplice Blog(Oracle) :- https://blogs.oracle.com/ksplice/entry/learning_by_doing_writing_your
Twisted Libraries(MIT) :- https://twistedmatrix.com/trac/

### Todos

 - Supporting the IPv6
 - Support for TCP,UDP
 - Add the GoogleMap APIs