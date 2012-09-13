#!/usr/bin/env python

import argparse

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class MitosisProtocol(LineReceiver):
    def __init__(self, nodes):
        self.nodes = nodes
        self.node_id = None
        self.identified = False

    def connectionMade(self):
        self.sendLine("Tell me your node id")

    def connectionLost(self, reason):
        if self.node_id in self.nodes:
            del self.nodes[self.node_id]
            self._notify_nodes("{} disconnected".format(self.node_id))

    def lineReceived(self, line):
        if not self.identified:
            self._register_node(line)

    def _register_node(self, node_id):
        if node_id in self.nodes:
            self.sendLine("Error: the node already exists")
            return
        self.sendLine("{} connected".format(node_id))
        self.node_id = node_id
        self.nodes[node_id] = self
        self.identified = True
        self._notify_nodes("{} connected".format(self.node_id))

    def _notify_nodes(self, message):
        for node, protocol in self.nodes.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class MitosisFactory(Factory):

    def __init__(self):
        self.nodes = {}  # maps node names for Mitosis instances

    def buildProtocol(self, addr):
        return MitosisProtocol(self.nodes)


if __name__ == '__main__':
    """
    For more information write: python mitosis.py -h
    """
    parser = argparse.ArgumentParser(
        description=('Creates a mitosis session'))
    parser.add_argument('-f', '--fun', action='store_true',
                        help='Fun parameter!!!!')
    arg_dict = vars(parser.parse_args())

    if arg_dict['fun']:
        print "Mitosis is funny!!!!!"

    tcp_port = 8123
    reactor.listenTCP(tcp_port, MitosisFactory())
    print "Running mitosis server in port {}".format(tcp_port)
    reactor.run()
