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
        # Create routers
        self.addNode('r110', cls=FRRRouter, loopback="100.100.1.1/32")
        self.addNode('r120', cls=FRRRouter, loopback="100.100.1.2/32")

        # Create hosts5
        self.addHost('h111', ip="10.1.1.1/24", defaultRoute=f'via 10.1.1.254')
        self.addHost('h121', ip="10.1.2.1/24", defaultRoute=f'via 10.1.2.254')

        # Link hosts to routers
        self.addLink('r110', 'h111', intfName1="r110-eth0", params1={"ip": "10.1.1.254/24"})
        self.addLink('r120', 'h121', intfName1="r120-eth0", params1={"ip": "10.1.2.254/24"})

        # Link routers
        self.addLink('r110', 'r120',
                     intfName1="r110-eth1", params1={"ip": "192.168.1.0/31"},
                     intfName2="r120-eth1", params2={"ip": "192.168.1.1/31"})


def startNetwork():
    info('*** Creating the network\n')
    topology = Topology()

    global net
    net = Mininet(topo=topology, link=Link, autoSetMacs=True)

    info('*** Starting the network\n')
    net.start()
    info('*** Running CLI\n')
    CLI(net)


def stopNetwork():
    if net is not None:
        net.stop()


if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
