
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import uuid
import queue
import rocksdb

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class MyReplicatorServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.db = rocksdb.DB("a2master.db", rocksdb.Options(create_if_missing=True))
        self.operations_queue = queue.Queue()

        def slave_replication(func):
            def wrapper_function(self, request, context):
                optn = datastore_pb2.SyncOperation(
                    optn=func.__name__,
                    key=request.key.encode(),
                    value=request.data.encode()
                )
                self.operations_queue.put(optn)
                return func(self, request, context)

            return wrapper_function

        def put(self, request, context):
            print("Put {}:{} to the master database".format(request.key, request.value))
            #saves key and value into DB converting request.data string to utf - 8 bytes
            self.db.put(request.key.encode(), request.value.encode())
            return datastore_pb2.Response(value='ok')

        def get(self, request, context):
            print("Get {} from the master database".format(request.key))
            # retrieves value into DB by the given key. Needs to convert request.key string to utf - 8 bytes
            value = self.db.get(request.key.encode())
            return datastore_pb2.Response(value=value)

        def delete(self, request, context):
            # deletes key from DB. Needs to convert request.key string to utf - 8 bytes
            print("Delete {} from the master database".format(request.key))
            self.db.delete(request.key.encode())
            return datastore_pb2.Response(value='ok')

        def replicate(self, request, context):
            # replicates value into the DB.
            print("Connection has been Established!")
            while True:
                operation = self.operations_queue.get()
                print("Sending operation ({}, {}, {}) to the slave database".format(operation.optn, operation.key, operation.value))
                yield operation

def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    datastore_pb2_grpc.add_MyReplicatorServicer_to_server(MyReplicatorServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 5000)
