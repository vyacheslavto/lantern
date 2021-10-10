from lantern_action import action
import xml.etree.cElementTree as eT
from time import sleep
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError
import logging
logger = logging.getLogger(__name__)


def xml_parse(xml_file):
    # set default parameters
    net_settings = dict(
        host="localhost",
        port=65000,
        buf_size=1024
    )
    command = dict()
    tree = eT.ElementTree(file=xml_file)
    _root = tree.getroot()
    for child in _root:
        if child.tag == "net_param":
            for step_child in child:
                net_settings.update({step_child.tag: step_child.text})
        if child.tag == "command":
            for step_child in child:
                command.update({step_child.tag: bytes([int(step_child.text, 16)])})
    return net_settings, command


def get_key(val, _dict):
    for key, value in _dict.items():
        if val == value:
            return key
    return False


@gen.coroutine
def get_request():
    global root
    net_setting, command = xml_parse("config.xml")
    while True:
        try:
            stream = yield TCPClient().connect(net_setting['host'], int(net_setting['port']))
            message = yield stream.read_bytes(int(net_setting['buf_size']), partial=True)
            stream.close()
            # def here
            command_type = get_key(bytes([message[0]]), command)
            if command_type:
                logger.warning(" Correct command: "+str(command_type))
                root = action(command_type, message, root)
            else:
                logger.warning(" Ignore incorrect command")
                sleep(3)
        except StreamClosedError:
            logger.warning(" No connection to the server")
            sleep(3)
        except Exception as e:
            logger.warning(e)
            break


if __name__ == "__main__":
    root = []
    IOLoop.current().run_sync(get_request)
