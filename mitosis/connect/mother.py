from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from mitosis.connect.mitconfig import MOTHER_HOST, MOTHER_PORT


class MotherProtocol(LineReceiver):
    def __init__(self, nodes):
        self.nodes = nodes
        self.node_id = None
        self.identified = False

    def connectionMade(self):
        """When the client connects"""
        self.sendLine("Tell me your node id")

    def connectionLost(self, reason):
        """When the client disconnects"""
        if self.node_id in self.nodes:
            del self.nodes[self.node_id]
            self._notify_nodes("{} disconnected".format(self.node_id))

    def lineReceived(self, line):
        if not self.identified:
            self._register_node(line)

    def _register_node(self, node_id):
        """Sets the node in the server list and notifies the connection to all
        the other nodes
        """
        if node_id in self.nodes:
            self.sendLine("Error: the node already exists")
            return
        self.sendLine("{} connected".format(node_id))
        self.node_id = node_id
        self.nodes[node_id] = self
        self.identified = True
        self._notify_nodes("{} connected".format(self.node_id))

    def _notify_nodes(self, message):
        """Sends a message to all the nodes"""
        for node, protocol in self.nodes.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class MotherFactory(Factory):
    def __init__(self):
        self.nodes = {}  # maps node names for Mitosis instances

    def buildProtocol(self, addr):
        return MotherProtocol(self.nodes)


def run():
    reactor.listenTCP(MOTHER_PORT, MotherFactory())
    print "Running mitosis mother in {}:{}".format(MOTHER_HOST, MOTHER_PORT)
    reactor.run()
