# -*- coding: utf-8 -*-
"""
https://github.com/emamirazavi/python3-ping
"""

# =============================================================================#
import argparse
import os
import sys
import socket
import struct
import select
import time
import signal

__description__ = 'A pure python ICMP ping implementation using raw sockets.'

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

NUM_PACKETS = 3
PACKET_SIZE = 64
WAIT_TIMEOUT = 3.0

# =============================================================================#
# ICMP parameters

ICMP_ECHOREPLY = 0  # Echo reply (per RFC792)
ICMP_ECHO = 8  # Echo request (per RFC792)
ICMP_MAX_RECV = 2048  # Max size of incoming buffer

MAX_SLEEP = 1000


class MyStats:
    thisIP = "0.0.0.0"
    pktsSent = 0
    pktsRcvd = 0
    minTime = 999999999
    maxTime = 0
    totTime = 0
    avrgTime = 0
    fracLoss = 1.0

myStats = MyStats  # NOT Used globally anymore.


# =============================================================================#
def checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    countTo = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if (sys.byteorder == "little"):
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        try:  # For Python3
            sum = sum + (hiByte * 256 + loByte)
        except:  # For Python2
            sum = sum + (ord(hiByte) * 256 + ord(loByte))
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string):  # Check for odd length
        loByte = source_string[len(source_string) - 1]
        try:  # For Python3
            sum += loByte
        except:  # For Python2
            sum += ord(loByte)

    sum &= 0xffffffff  # Truncate sum to 32 bits (a variance from ping.c, which
    # uses signed ints, but overflow is unlikely in ping)

    sum = (sum >> 16) + (sum & 0xffff)  # Add high 16 bits to low 16 bits
    sum += (sum >> 16)  # Add carry from above (if any)
    answer = ~sum & 0xffff  # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer


# =============================================================================#
def do_one(myStats, destIP, hostname, timeout, mySeqNumber, packet_size, quiet=False):
    """
    Returns either the delay (in ms) or None on timeout.
    """
    delay = None

    try:  # One could use UDP here, but it's obscure
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    except socket.error as e:
        print("failed. (socket error: '%s')" % e.args[1])
        raise  # raise the original error

    my_ID = os.getpid() & 0xFFFF

    sentTime = send_one_ping(mySocket, destIP, my_ID, mySeqNumber, packet_size)
    if sentTime == None:
        mySocket.close()
        return delay

    myStats.pktsSent += 1

    recvTime, dataSize, iphSrcIP, icmpSeqNumber, iphTTL = receive_one_ping(mySocket, my_ID, timeout)

    mySocket.close()

    if recvTime:
        delay = (recvTime - sentTime) * 1000
        if not quiet:
            print("%d bytes from %s: icmp_seq=%d ttl=%d time=%d ms" % (
                dataSize, socket.inet_ntoa(struct.pack("!I", iphSrcIP)), icmpSeqNumber, iphTTL, delay)
                  )
        myStats.pktsRcvd += 1
        myStats.totTime += delay
        if myStats.minTime > delay:
            myStats.minTime = delay
        if myStats.maxTime < delay:
            myStats.maxTime = delay
    else:
        delay = None
        print("Request timed out.")
    return delay


# =============================================================================#
def send_one_ping(mySocket, destIP, myID, mySeqNumber, packet_size):
    """
    Send one ping to the given >destIP<.
    """
    # destIP  =  socket.gethostbyname(destIP)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    # (packet_size - 8) - Remove header size from packet size
    myChecksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, myChecksum, myID, mySeqNumber
    )

    padBytes = []
    startVal = 0x42
    # 'cose of the string/byte changes in python 2/3 we have
    # to build the data differnely for different version
    # or it will make packets with unexpected size.
    if sys.version[:1] == '2':
        bytes = struct.calcsize("d")
        data = ((packet_size - 8) - bytes) * "Q"
        data = struct.pack("d", default_timer()) + data
    else:
        for i in range(startVal, startVal + (packet_size - 8)):
            padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        # data = bytes(padBytes)
        data = bytearray(padBytes)

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)  # Checksum is in network order

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, myChecksum, myID, mySeqNumber
    )

    packet = header + data

    sendTime = default_timer()

    try:
        mySocket.sendto(packet, (destIP, 1))  # Port number is irrelevant for ICMP
    except socket.error as e:
        print("General failure (%s)" % (e.args[1]))
        return

    return sendTime


# =============================================================================#
def receive_one_ping(mySocket, myID, timeout):
    """
    Receive the ping from the socket. Timeout = in ms
    """
    timeLeft = timeout / 1000

    while True:  # Loop while waiting for packet or timeout
        startedSelect = default_timer()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (default_timer() - startedSelect)
        if whatReady[0] == []:  # Timeout
            mySocket.settimeout(timeout)
            # return None, 0, 0, 0, 0

        timeReceived = default_timer()

        recPacket, addr = mySocket.recvfrom(ICMP_MAX_RECV)

        ipHeader = recPacket[:20]
        iphVersion, iphTypeOfSvc, iphLength, \
        iphID, iphFlags, iphTTL, iphProtocol, \
        iphChecksum, iphSrcIP, iphDestIP = struct.unpack(
            "!BBHHHBBHII", ipHeader
        )

        icmpHeader = recPacket[20:28]
        icmpType, icmpCode, icmpChecksum, \
        icmpPacketID, icmpSeqNumber = struct.unpack(
            "!BBHHH", icmpHeader
        )

        if icmpPacketID == myID:  # Our packet
            dataSize = len(recPacket) - 28
            # print (len(recPacket.encode()))
            return timeReceived, (dataSize + 8), iphSrcIP, icmpSeqNumber, iphTTL

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return None, 0, 0, 0, 0


# =============================================================================#
def dump_stats(myStats):
    """
    Show stats when pings are done
    """
    print("\n----%s PYTHON PING Statistics----" % (myStats.thisIP))

    if myStats.pktsSent > 0:
        myStats.fracLoss = (myStats.pktsSent - myStats.pktsRcvd) / myStats.pktsSent

    print("%d packets transmitted, %d packets received, %0.1f%% packet loss" % (
        myStats.pktsSent, myStats.pktsRcvd, 100.0 * myStats.fracLoss
    ))

    if myStats.pktsRcvd > 0:
        print("round-trip (ms)  min/avg/max = %d/%0.1f/%d" % (
            myStats.minTime, myStats.totTime / myStats.pktsRcvd, myStats.maxTime
        ))

    print("")
    return


# =============================================================================#
def signal_handler(signum, frame):
    """
    Handle exit via signals
    """
    dump_stats()
    print("\n(Terminated with signal %d)\n" % (signum))
    sys.exit(0)


# =============================================================================#
def verbose_ping(hostname, timeout=WAIT_TIMEOUT, count=NUM_PACKETS,
                 packet_size=PACKET_SIZE, path_finder=False):
    """
    Send >count< ping to >destIP< with the given >timeout< and display
    the result.
    """
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl-C
    if hasattr(signal, "SIGBREAK"):
        # Handle Ctrl-Break e.g. under Windows
        signal.signal(signal.SIGBREAK, signal_handler)

    myStats = MyStats()  # Reset the stats

    mySeqNumber = 0  # Starting value

    try:
        destIP = socket.gethostbyname(hostname)
        print("\nPYTHON PING %s (%s): %d data bytes" % (hostname, destIP, packet_size))
    except socket.gaierror as e:
        print("\nPYTHON PING: Unknown host: %s (%s)" % (hostname, e.args[1]))
        print()
        return

    myStats.thisIP = destIP

    for i in range(count):
        delay = do_one(myStats, destIP, hostname, timeout, mySeqNumber, packet_size)

        if delay == None:
            delay = 0

        mySeqNumber += 1

        # Pause for the remainder of the MAX_SLEEP period (if applicable)
        if (MAX_SLEEP > delay):
            time.sleep((MAX_SLEEP - delay) / 1000)

    dump_stats(myStats)


# =============================================================================#
def quiet_ping(hostname, timeout=WAIT_TIMEOUT, count=NUM_PACKETS,
               packet_size=PACKET_SIZE, path_finder=False):
    """
    Same as verbose_ping, but the results are returned as tuple
    """
    myStats = MyStats()  # Reset the stats
    mySeqNumber = 0  # Starting value

    try:
        destIP = socket.gethostbyname(hostname)
    except socket.gaierror as e:
        return False

    myStats.thisIP = destIP

    # This will send packet that we dont care about 0.5 seconds before it starts
    # acrutally pinging. This is needed in big MAN/LAN networks where you sometimes
    # loose the first packet. (while the switches find the way... :/ )
    if path_finder:
        fakeStats = MyStats()
        do_one(fakeStats, destIP, hostname, timeout,
               mySeqNumber, packet_size, quiet=True)
        time.sleep(0.5)

    for i in range(count):
        delay = do_one(myStats, destIP, hostname, timeout,
                       mySeqNumber, packet_size, quiet=True)

        if delay == None:
            delay = 0

        mySeqNumber += 1

        # Pause for the remainder of the MAX_SLEEP period (if applicable)
        if (MAX_SLEEP > delay):
            time.sleep((MAX_SLEEP - delay) / 1000)

    if myStats.pktsSent > 0:
        myStats.fracLoss = (myStats.pktsSent - myStats.pktsRcvd) / myStats.pktsSent
    if myStats.pktsRcvd > 0:
        myStats.avrgTime = myStats.totTime / myStats.pktsRcvd

    # return tuple(max_rtt, min_rtt, avrg_rtt, percent_lost)
    return myStats.maxTime, myStats.minTime, myStats.avrgTime, myStats.fracLoss


def Ping(hostname, timeout=3, count=2):
    myStats = MyStats()

    try:
        destIP = socket.gethostbyname(hostname)
    except socket.gaierror as e:
        print(e)
        return

    myStats.thisIP = destIP

    for i in range(count):
        try:
            delay = do_one(myStats, destIP, hostname, timeout, i, PACKET_SIZE)
            print(delay)
        except Exception as err:
            print("failed. %s " % err)
            continue

        if delay == None:
            continue
        else:
            return True
    return False


# =============================================================================#
def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='quiet output')
    parser.add_argument('-c', '--count', type=int, default=NUM_PACKETS,
                        help=('number of packets to be sent '
                              '(default: %(default)s)'))
    parser.add_argument('-W', '--timeout', type=float, default=WAIT_TIMEOUT,
                        help=('time to wait for a response in seoncds '
                              '(default: %(default)s)'))
    parser.add_argument('-s', '--packet-size', type=int, default=PACKET_SIZE,
                        help=('number of data bytes to be sent '
                              '(default: %(default)s)'))
    parser.add_argument('destination')
    args = parser.parse_args()

    ping = verbose_ping
    if args.quiet:
        ping = quiet_ping

    ping(args.destination, timeout=args.timeout * 1000, count=args.count, packet_size=args.packet_size)


if __name__ == '__main__':
    a = Ping('172.30.72.77', 5, 10)
    print(a)
    # main()
