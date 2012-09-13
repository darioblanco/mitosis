#!/usr/bin/env python

from sys import stdout

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

from mitosis.connect.mitconfig import MOTHER_HOST, MOTHER_PORT


class DaughterProtocol(Protocol):
    def dataReceived(self, data):
        stdout.write(data)


class DaughterFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return DaughterProtocol()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)


def run():
    reactor.connectTCP(MOTHER_HOST, MOTHER_PORT, DaughterFactory())
    print "Running mitosis daughter in port {}".format(MOTHER_PORT)
    reactor.run()
