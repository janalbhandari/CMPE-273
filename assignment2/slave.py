import grpc
import datastore_pb2
import argparse
import rocksdb

PORT = 3000


class MySlaveReplicator():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.db = rocksdb.DB("a2slave.db", rocksdb.Options(create_if_missing=True))
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)

    def rep(self):
        replicator = self.stub.rep(datastore_pb2.RepRequest())
        print("Connected established with master!")
        for optn in replicator:
            if optn.optn == 'put':
                print("Put {}:{} into slave db".format(optn.key, optn.data))
                self.db.put(optn.key.encode(), optn.data.encode())
            elif optn.optn == 'delete':
                print("Delete {} from slave db".format(optn.key))
                self.db.delete(optn.key.encode())
            else:
                # invalid operation
                pass



def main():


    slave = MySlaveReplicator()
    slave.rep()


if __name__ == "__main__":
    main()

