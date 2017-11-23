# Python replicator

# Generate the proto file :

  python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto

# Run master(server) :

  python3.6 master.py

# Run slave :

  python3.6 slave.py

# Run test case : 

  python3.6 test.py
