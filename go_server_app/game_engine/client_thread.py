from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue, Empty

# from eyalarubas.com/python-subproc-nonblock.html
# TODO wire this up to gnugo


class NonBlockingStreamReader:
    def __init__(self, stream):
        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target=_populateQueue, args=(self._s, self._q))
        self._t.daemon = True
        self._t.start()

    def readline(self, timeout=None):
        try:
            return self._q.get(block=timeout is not None, timeout=timeout)
        except Empty:
            return None


class UnexpectedEndOfStream(Exception):
    pass


# run the shell as a subprocess:

p = Popen(['python', 'shell.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
# wrap p.stdout with a NonBlockingStreamReader object:
nbsr = NonBlockingStreamReader(p.stdout)
# issue command:
p.stdin.write(b'command\n')
# get the output
while True:
    # 0.1 secs to let the shell output the result
    output = nbsr.readline(0.1)
    if not output:
        print('[No more data]')
        break
    print(output)
