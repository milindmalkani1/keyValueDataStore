import threading
import json
import os
import time

'''
search for a particular key in the file and converts the entire file
in a python dict obj, will also be use-full
during the reading of a particular key and checking if a key
is present inside the dictionary or not
'''


def searchKey(keyForSearching, givenPathS):
    d = {}
    with open(os.path.join(givenPathS, 'test.txt'), 'r') as fp:
        for line in fp:
            splitTimeKey = line.split(":")  # splitting the line with (key,value) and (time)
            splitKeyValue = splitTimeKey[0].split("-")  # splitting the line with (key) and (value)
            (key, val, givenTime) = splitKeyValue[0], splitKeyValue[1], splitTimeKey[1]  # storing temp in a tuple
            d[key] = val, givenTime  # storing in the dictionary

    if keyForSearching in d:
        global value  # global variable to get the value so that we can use this further while reading/del in the file
        value = d[keyForSearching][0]
        global timeValue  # to get the time value associated with the key to use while reading/deleting
        timeValue = float(d[keyForSearching][1])
        return True
    else:
        return False


'''
create function takes the given path and an optional
time to live value for the key
'''


def create(givenPath, lck, ttl=0):
    lck.acquire()
    key = input("Enter the key to be inserted: ")
    if searchKey(key, givenPath):
        print("Error:Key is already present in the file.")
    else:
        jsonValue = input("Enter the value to the corresponding key: ")
        # deserializedJson = json.load(jsonValue)

        fileStats = os.stat(os.path.join(givenPath, 'test.txt'))  # getting the fileStats
        fileSize = fileStats.st_size  # getting the file size

        if len(key) > 32 or len(jsonValue) > 16 * 1024:  # checking if the len of the key > 32 chars/JSON Value > 16KB
            print("Error:Invalid input format of key and value.")
        elif fileSize > 1024 * 1024 * 1024:  # if anytime the size of the file exceeds 1GB
            print("Error:File Size has exceeded more than a GB cannot enter more.")
        else:
            with open(os.path.join(givenPath, 'test.txt'), 'a+') as fp:  # writing given key value to the file
                internalFileSize = os.path.getsize(os.path.join(givenPath, 'test.txt'))
                if internalFileSize > 0:
                    fp.write("\n")
                if ttl == 0:
                    fp.write(key + "-" + jsonValue + ":" + str(ttl))
                else:
                    fp.write(key + "-" + jsonValue + ":" + str(time.time() + ttl))
    lck.release()


'''
read function will take the given path of the file
and reads the inputted key and returns the corresponding value
'''


def read(givenPath, lck):
    lck.acquire()
    key = input("Enter the key of which corresponding value you want to read: ")

    if searchKey(key, givenPath):
        if timeValue != 0 and time.time() > timeValue:
            print("Error:Time to live value of the key has expired.")
        else:
            json.dumps(value)  # for the serialization of the python object
            print("The value is: " + value)
    else:
        print("Error:Key is not preset in the file.")
    lck.release()


'''
delete the given key vale pair from the file
this function will take the given path as ip
'''


def delete(givenPath, lck):
    lck.acquire()
    key = input("Enter the key whose key value pair you want to delete: ")
    if searchKey(key, givenPath):
        if timeValue != 0 and time.time() > timeValue:
            print("Error:Time to live value of the key has expired.")
        else:
            with open(os.path.join(givenPath, 'test.txt'), 'r') as fp:
                data = fp.readlines()
            with open(os.path.join(givenPath, 'test.txt'), 'w') as fp:
                for line in data:
                    if not (line.startswith(key)):
                        fp.write(line)
    else:
        print("Error:Key is not present in the file.")
    lck.release()


if __name__ == '__main__':
    lock = threading.Lock()
    path = input('Enter the path of the file: ')
    if path:
        file = open(os.path.join(path, 'test.txt'), 'a')
        file.close()
    else:
        file = open('test.txt', 'a')
        file.close()

    # threads = []
    # for i in range(0, 50):
    #     ar = (givenPath, lck, ttl)
    #     t = threading.Thread(target=create, args=ar)
    #     threads.append(t)
    #     t.start()
    #
    # for t in threads:
    #     t.join()

    # usage of different functionalities calling respective functions with the path and lock as arguments
    create(path, lock)
    read(path, lock)
    delete(path, lock)
