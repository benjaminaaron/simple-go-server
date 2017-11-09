import sys

# from eyalarubas.com/python-subproc-nonblock.html
# this is a dummy process as proof of concept for client_thread

while True:
    s = input("Enter command: ")
    print("You entered: {}".format(s))
    sys.stdout.flush()
