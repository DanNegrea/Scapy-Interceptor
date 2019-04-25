# Scapy-Interceptor
Intercept and edit packets on the fly using your preffered code editor.
The packets are represented in *Scapy* syntax. The interception is done using *NetfilterQueue* & *iptables*.

## Two variants:

1. Text Mode (currently opening *vim*)
2. GUI (on the pipeline)


### Example
Demonstrates how to replace the destination IP address (93.184.216.255 -> 93.184.216.34) of an Echo (ping) request.
This will ping *example.com*.

#### Add iptable rule
Forward all packets destined for 93.184.216.255 to the 2nd NFQUEUE
'''
iptables -I OUTPUT -d 93.184.216.255 -j NFQUEUE --queue-num 2
'''

#### Call Scapy-Interceptor
'''
python3 Scapy-Interceptor-txt.py
'''

#### Ping the target
... in a new terminal.
```
root@kali:~# ping -c 1 93.184.216.255
```
#### Edit the packet
1. Return to the Scapy-Interceptor tab
2. Replace 225 with 34 (for example using: `:s/255/34/g`)
3. Save and exit (`:wq`)

#### See the ping result
```
root@kali:~# ping -c 1 93.184.216.255
PING 93.184.216.255 (93.184.216.255) 56(84) bytes of data.
64 bytes from 93.184.216.34: icmp_seq=1 ttl=53 time=9184 ms
```

### Requirements

#### Linux OS
Was tested on Kali

#### Scapy
[https://scapy.net/](https://scapy.net/)

#### Netfilterqueue 
[https://pypi.org/project/NetfilterQueue/](https://pypi.org/project/NetfilterQueue/)

In Python 3.7 must be [buid manually](https://github.com/kti/python-netfilterqueue/issues/48).
These steps worked for me:
```
pip3 install Cython
apt-get install build-essential python-dev libnetfilter-queue-dev
git clone https://github.com/kti/python-netfilterqueue.git
cd python-netfilterqueue
python3 setup.py build_ext --force
python3 setup.py install
```
