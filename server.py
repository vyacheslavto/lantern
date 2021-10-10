import xml.etree.cElementTree as eT
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpserver import TCPServer


def xml_parse(xml_file):
    _port = 65000
    _command = dict()
    tree = eT.ElementTree(file=xml_file)
    root = tree.getroot()
    for child in root:
        if child.tag == "net_param":
            for step_child in child:
                if step_child.tag == "port":
                    _port = int(step_child.text)
        if child.tag == "command":
            for step_child in child:
                _command.update({step_child.tag: bytes([int(step_child.text, 16)])})
    return _port, _command


class EchoServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        a = True
        while a:
            try:
                global temp
                yield stream.write(temp)
                a = False
            except Exception as e:
                print(e)
        IOLoop.current().stop()


if __name__ == "__main__":
    port, command = xml_parse('config.xml')
    temp = b'\x12\x00\x03\x00\x00\xff'
    test_server = EchoServer()
    test_server.listen(port)
    IOLoop.current().start()
