'''
# Assignment 2 (test case)
'''

import grpc
import datastore_pb2

class Test():
    def __init__(self, host, port):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)

    def put(self, key, data):
        return self.stub.put(datastore_pb2.Request(key=key, value=value))

    def delete(self, key):
        return self.stub.delete(datastore_pb2.Request(key=key))

# Code to run a process listening at port 5000
def run(host, port):
    '''
    Run the GRPC server
    '''
    test = Test(host, port)

    print('key = key1, value = value1')
    response = test.put('key1', 'value1')
    print(response.value == '0' if 'HTTP 200 OK' else "Failed")
    print('delete key = value1')
    response = test.delete('value1')
    print(response.value == '0' if 'HTTP 200 OK' else "Failed")

if __name__ == '__main__':
    run('0.0.0.0', 5000)