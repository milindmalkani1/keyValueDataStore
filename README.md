# File Based Key-Value Data Store(CRD)
This is a file which can be used as a data store that supports the basic CRD(create, read, write) operations. Data store is meant to be used as a local storage for one single process on one laptop.

# Getting Started

## Requirements
* Python 3

## Features
The Key-Value Data Store will support following funcionality:
1. It can be initialized using an optional file path. If one is not provided, it will reliably create itself in a reasonable location on the laptop.
2. A new key-value pair can be added to the data store using the Create operation. The key is always a string - capped at 32chars. The value is always a JSON object - capped at 16 KB.
3. If Create is invoked for an existing key, an appropriate error will be returned.
4. A Read operation on a key can be performed by providing the key, and receiving the value in response, as a JSON object.
5. A Delete operation can be performed by providing the key.
6. Every key supports setting a Time-To-Live property when it is created. This property is optional. If provided, it will be evaluated as an integer defining the number of seconds the key will be retained in the data store. Once the Time-To-Live for a key has expired, the key will no longer be available for Read or Delete operations.
7. Appropriate error responses will always be returned to a client if it uses the data store in unexpected ways or breaches any limits.
8. The file size never exceeds 1 GB.
9. The file can also be accessed using multiple threads.

# Built With
* Python

## Accessing
Run main.py and you can use every functionality by calling different functions inside main.py, passing path(refer to point 1) and lock as arguments, where path will be optional if not given the file will be created in the dir where scripts are.
