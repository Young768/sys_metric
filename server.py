from os.path import join, isfile, abspath
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import Fault, ServerProxy
from urlparse import urlparse
import sys

MAX_HISTORY_NODE_LENGTH = 6 #Node Length
UNHANDLED_CODE = 100 # Return Code
ACCESS_DENIED_CODE = 200 #Return Code

SimpleXMLRPCServer.allow_reuse_address = 1 #Port reuse
class UnhandledQuery(Fault):
    '''
       That's show can't handle the query exception
       '''
    def __init__(self, message="Couldn't handle the query"):
        super(UnhandledQuery, self).__init__(UNHANDLED_CODE, message)

class AccessDenied(Fault):
    '''
       When user try to access the forbiden resources raise exception
       '''
    def __init__(self, message="Access denied"):
        super(AccessDenied, self).__init__(ACCESS_DENIED_CODE, message)

def inside(dir, name):
##'''
##       Check the dir that user defined is contain the filename which the user given
##    '''
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ''))

def getPort(url):
##    '''
##       Get the port from the url
##       '''
    name = urlparse(url)[1] # '127.0.0.1:9090'
    port = int(name.split(':')[1])
    return port

class Node(object):
    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname = dirname
        self.secret = secret
        self.known = set()

    def query(self, query, history=[]):
        try:
            return self._handle_request(query)
        except UnhandledQuery: #No file in local node
            history = history + [self.url]
            if len(history) > MAX_HISTORY_NODE_LENGTH:
                raise
            return self._boardcast(query, history)

    def hello(self, other):
#        '''
#               Hello to other nodes
#               '''
        self.known.add(other)
        return 0

    def fetch(self, query, secret):
#       '''
#               find the file to download
#               '''
        if secret != self.secret:
            raise AccessDenied
        result = self.query(query)
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close
        return 0

    def _start_rpc_server(self):
            s = SimpleXMLRPCServer(('', getPort(self.url)))
            s.register_instance(self)
            s.serve_forever()

    def _handle_request(self, query):
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name):
            raise UnhandledQuery
        if not inside(dir, name):
            raise AccessDenied

        return open(name).read()

    def _boardcast(self, query, history):
        for other in self.known.copy():
            if other in history:
                continue
            try:
                s = ServerProxy(other)
                return s.query(query, history) # Other nodes to invoke the RPC SERVER Method
            except Fault as f: #Fault init function has "faultCode and faultString"
                if f.faultCode == UNHANDLED_CODE:
                    pass
                else:
                    self.known.remove(other)
            except:
                self.known.remove(other)
        raise UnhandledQuery

def main():
    url, directory, secret = sys.argv[1:]
    n = Node(url, directory, secret)
    n._start_rpc_server()

if __name__ == "__main__":
    main()
