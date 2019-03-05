#/usr/bin/env python2.7


from cmd import Cmd
from xmlrpclib import ServerProxy, Fault
from random import choice
from string import lowercase
from server import Node, UNHANDLED_CODE
from threading import Thread
from time import sleep

import sys

HEAD_START = 0.1
SECRET_LENGTH = 100

def randomString(length):
    chars = []
    letters = lowercase[:26] # return 'abcdefghijklmnopqrstuvwxyz'
    while length>0:
            chars.append(choice(letters))
            length -= 1
    return ''.join(chars)

class Client(Cmd):
    prompt = 'yang_terminal_cmd> '

    def __init__(self, url, dirname, urlfile):
        Cmd.__init__(self)
        self.secret = randomString(SECRET_LENGTH)
        n = Node(url, dirname, self.secret)
        t = Thread(target=n._start_rpc_server)
        t.setDaemon(1)
        t.start()

        sleep(HEAD_START)
        self.server = ServerProxy(url)

        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)

    def do_fetch(self, arg):
        try:
            self.server.fetch(arg, self.secret)
        except Fault as f:
            if f.faultCode != UNHANDLED_CODE:
                raise



    def do_exit(self, arg):
        print ()
        sys.exit()
        do_EOF = do_exit

def main():
    urlfile, directory, url = sys.argv[1:]
    print(urlfile,directory,url)
    client = Client(url, directory, urlfile)
    client.cmdloop()

if __name__ == "__main__":
    main()
