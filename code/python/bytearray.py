import threading

""" This shows how you can use a bytearray to pass data between a main program
and a thread. Since bytearrays are mutable, they can be used to move data in
both directions.
"""

def writer_thread(arg: bytearray):
    print(hex(id(arg)))
    arg.clear()
    arg.extend(b"ciao")

def main():
    b_array = bytearray()
    print(hex(id(b_array)))
    t = threading.Thread(target=writer_thread, args=(b_array,))
    t.start()
    t.join()
    assert bytes(b_array) == b"ciao"

if __name__ == "__main__":
    main()
