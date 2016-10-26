class NewLineTerminatorBuffer(object):
    def __init__(self, buffer):
        self.buffer = buffer

    def write(self, line):
        self.buffer.write(line, ending='')
