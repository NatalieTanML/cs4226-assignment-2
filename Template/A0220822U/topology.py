import atexit

from mininet.cli import CLI
from mininet.link import Link
from mininet.log import info, setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from router import FRRRouter

net = None


class Topology(Topo):
    def build(self):
        # Add your code here
        pass


def startNetwork():
    info("*** Creating the network\n")
    topology = Topology()

    global net
    net = Mininet(topo=topology, link=Link, autoSetMacs=True)

    info("*** Starting the network\n")
    net.start()
    info("*** Running CLI\n")
    CLI(net)


def stopNetwork():
    if net is not None:
        net.stop()


if __name__ == "__main__":
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel("info")
    startNetwork()