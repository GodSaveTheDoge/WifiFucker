# WifiFucker

*A tool to do arp poisoning*



## What does it do

Simply spams arp responses to make a device use the desired mac address instead of the router mac address.



## Usage

```
Usage: main.py [OPTIONS] VICTIM_IP ROUTER_IP

Arguments:
  VICTIM_IP  The ip of the victim device  [required]
  ROUTER_IP  The ip of the router  [required]

Options:
  --delay FLOAT             The delay between packets  [default: 5.0]
  --mac-addr TEXT           The mac address to send to the victim  [default:
                            (random)]

  --restore / --no-restore  Send the real mac address before quitting
                            [default: False]

  --help                    Show this message and exit.
```

**Example:**

Sends packets to `192.168.1.174` poisoning the mac address of `192.168.1.1` every 0.5 seconds and, before stopping, sends the real mac address.

`python3 main.py 192.168.1.174 192.168.1.1 --restore --delay 0.5`



## How to install it

Try to do it on your own.
