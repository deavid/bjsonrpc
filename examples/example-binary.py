# encoding: UTF-8
import sys
sys.path.insert(0,"../") # prefer local version

import bjsonrpc
from bjsonrpc.jsonlib import j as json
import quopri
import base64

# Binary data test 1: 10 bits pure random data.

def test(data):
    print "### Testing:", repr(data)
    # Binary pure data:
    try:
        bindata1 = data
        json_bindata1 = json.dumps(bindata1)
        print "Binary 8-bit:", json_bindata1
    except Exception, e: 
        print e
        print "Binary 8-bit: -- unable to create a json string from binary data --"

    # Quoted-printable:
    try:
        bindata1 = quopri.encodestring(data)
        json_bindata1 = json.dumps(bindata1)
        print "Quoted-printable:", json_bindata1
    except Exception, e: 
        print e
        print "Quoted-printable: -- unable to create a json string from binary data --"
    
    # Base64:
    try:
        bindata1 = base64.b64encode(data)
        json_bindata1 = json.dumps(bindata1)
        print "Base64:", json_bindata1
    except Exception, e: 
        print e
        print "Base64: -- unable to create a json string from binary data --"
    

random_data = 'faL\xcb\x05\x11f\xdc\x17>\x9c\x15Y^\xb5\xad\x1f\x1fY='
lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean est mauris, blandit quis luctus et, fermentum non velit. Aliquam dapibus placerat sagittis. Maecenas nisi ligula, ultrices sed elementum vel, adipiscing vitae nunc. Aenean consectetur, turpis et mollis molestie, urna augue ultrices tortor, commodo lacinia dui augue in arcu. Curabitur vel metus nibh. Integer sed lectus ut velit dapibus consequat. Integer ipsum ante, ultricies dignissim elementum vitae, interdum sit amet velit. Vestibulum et mauris arcu. In porta rutrum commodo. Nam nibh tellus, placerat ultricies blandit vel, adipiscing eu arcu. Nam nec dolor ut sem ultricies iaculis. Nam ornare lobortis placerat. Quisque commodo lobortis aliquet. Duis id libero felis.
Nulla at sapien turpis, vel auctor leo. Sed id pellentesque justo. Sed tempus justo et metus auctor nec vulputate felis tempor. Donec congue sodales nibh pharetra feugiat. Duis eget dictum erat. Vestibulum sollicitudin volutpat suscipit. Mauris feugiat sodales turpis ac placerat. Integer ac elit eu eros tincidunt pretium. Proin posuere sodales tortor quis dignissim. Maecenas quis lorem ac magna gravida sodales. Fusce at leo in magna convallis volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Curabitur eu enim purus. Etiam ac arcu posuere velit lacinia lacinia ut vitae enim. Suspendisse potenti.
Morbi egestas magna at metus lobortis ut aliquet metus cursus. In hac habitasse platea dictumst. Suspendisse potenti. Nulla ultricies, erat in sollicitudin aliquam, metus urna cursus est, a ultrices nulla ante sed turpis. In fringilla libero egestas nisi convallis ultricies. Vestibulum diam ipsum, tincidunt sit amet lacinia non, auctor id ante. Quisque pulvinar dapibus risus sit amet venenatis. Suspendisse aliquam diam vel enim cursus et consequat odio venenatis. Sed sit amet leo eget orci aliquam rutrum.
Pellentesque ante libero, porttitor vel auctor vitae, sagittis ac turpis. Mauris vel nibh nec ante adipiscing vehicula. Cras id orci diam, varius ornare nunc. Suspendisse ac neque ac ante volutpat rutrum. Nunc facilisis aliquam sollicitudin. Sed mauris eros, sagittis nec mollis eu, fringilla feugiat arcu. Vivamus vitae odio nunc. Donec nisl libero, blandit in egestas in, gravida ut ipsum.
"""
lorem_ipsum2 = """Maecenas mauris orci, lacinia aliquet dignissim aliquet, facilisis sit amet tortor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer commodo, magna sit amet vulputate porttitor, metus risus elementum nunc, sed sagittis mi eros molestie nunc. Aliquam erat volutpat. Sed viverra lectus et tellus scelerisque id iaculis urna fermentum. Nullam ut neque nisi, at iaculis neque. Pellentesque vitae arcu nec odio tincidunt egestas.
Aliquam aliquet risus metus. Nulla sodales dictum nisi, in interdum purus tincidunt vitae. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Phasellus ultricies viverra est, sed dapibus mi mattis id. Nullam blandit, dolor quis vehicula pretium, ipsum sem pretium tortor, et sodales metus sapien et lectus. Donec eu quam eros. Suspendisse non diam velit. Aliquam vestibulum egestas turpis, consequat pellentesque urna gravida a. Praesent tincidunt nisl et lectus dictum lobortis sit amet sed lacus. Fusce ligula metus, elementum et imperdiet eu, auctor eu leo. Quisque eu purus velit. Mauris tempus imperdiet dictum. Pellentesque porttitor orci nunc, eget sodales tellus.
Integer nec lorem nisl. Nullam consequat vulputate lacus, nec ullamcorper mauris tincidunt vel. Nulla sollicitudin consectetur purus, eu adipiscing velit adipiscing non. Praesent eget nisi est, ac auctor libero. Etiam varius eros et velit convallis porta. Suspendisse fringilla ligula enim. Suspendisse non urna ac mi congue imperdiet. Quisque nulla est, bibendum non pulvinar commodo, egestas non eros. Praesent ornare, lorem vel sodales aliquet, tellus ligula malesuada dolor, at vehicula ipsum dolor sit amet tellus. Sed tristique odio nec felis pulvinar porttitor. Proin a orci velit. Cras dignissim odio vitae magna dapibus egestas. Nulla eleifend odio sit amet quam ultrices eu molestie elit vulputate. Phasellus in lacus ac risus bibendum eleifend a sed lectus. In venenatis malesuada arcu, a faucibus mauris sagittis eu. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Donec non semper ligula. Nulla facilisi. Proin placerat, ante fringilla iaculis commodo, diam libero pretium arcu, eget euismod ante nibh vitae metus. Integer et dui augue, nec tincidunt tortor. Donec a ornare tellus. Suspendisse potenti. Nulla lectus purus, egestas eget rhoncus pellentesque, luctus vitae risus. Pellentesque ultrices tellus quis est porttitor eget faucibus nisi pretium. Nunc laoreet dapibus faucibus. Ut faucibus, odio nec lobortis rhoncus, nibh quam facilisis elit, id dignissim tellus dolor in velit. Donec nulla dolor, semper et imperdiet at, dictum sit amet purus. Vestibulum at varius odio. Integer tincidunt dui nec lorem fermentum facilisis.
Donec pellentesque dolor vel ante sollicitudin facilisis. Morbi pharetra, mauris in dignissim gravida, leo lorem mollis tortor, quis tempus purus tortor sit amet erat. Phasellus dignissim mollis velit ut condimentum. Nullam porta tincidunt ligula in placerat. Donec nisl turpis, laoreet a auctor a, eleifend id enim. Vivamus non sem sit amet nunc sagittis faucibus vel a diam. In vestibulum massa non metus tempus blandit. Proin pellentesque, elit vitae auctor feugiat, felis orci fermentum enim, eu lacinia augue ligula ac turpis. Etiam ut neque ac dui feugiat placerat. Proin lobortis neque eget dui tincidunt quis bibendum quam blandit. Nulla id nisl non risus pulvinar pellentesque. In tempor ligula egestas diam adipiscing faucibus interdum ipsum hendrerit.
"""
#test("Hello world")
#test("hùpst holten jede.\nzerteilen pumpst wö ziemt las.\n")
#test(random_data)

from bjsonrpc.binary import BinaryData
import yaml
import os
print "Creating random-data . . ."
big_random_data = os.urandom(1024*1024) # 1Mb pure-random data.
print "done."
for i in range(5):
    big_random_data += big_random_data
    print "Size: %.2fMB" % (len(big_random_data) / 1024.0 / 1024.0)
print "Encoding data . . . " 
x = BinaryData(big_random_data,encoding="zlib-base64")

#x = BinaryData(random_data,encoding="base64")
#x = BinaryData(lorem_ipsum,encoding="zlib-base64")
#x = BinaryData(lorem_ipsum,encoding="base64")
#x = BinaryData(random_data,encoding="base64",digest="sha224:base64:len4",dump_mode="short")
#x = BinaryData(random_data,encoding="base64",digest="sha224:base64:len4",dump_mode="standard")
#x = BinaryData(lorem_ipsum[:100],encoding="quopri",digest="sha1:base64:")
print "done." 
print yaml.dump(x.format())
print "Dumping data as JSON:"
dumped = json.dumps(x.dump(),separators = (',', ':'))
print "Loading JSON:"
loaded = BinaryData(jsonobj=json.loads(dumped))
print "Some tests..."
assert('\n' not in dumped)
print "done."
# ---- Test with a real connection:
import threading, time
from bjsonrpc.handlers import BaseHandler

RPC_PORT = 10123
class MyHandler(BaseHandler):
    def _setup(self):
        self.file1 = ""
    
    def save_bindata(self, bindata):
        print "Received bindata, decoding . . ."
        loaded = BinaryData(jsonobj=bindata)
        print "done decoding."
        self.file1 = loaded.data
        return loaded.digest
    
    def stop(self):
        sys.exit(0)
        
def thread1():  
    time.sleep(0.2)  # -> Wait for server start.
    print "Conecting to server . . ."
    conn = bjsonrpc.connect(host="127.0.0.1",port=RPC_PORT)
    print "Sending data . . ."
    digest =  conn.call.save_bindata(x.dump())
    print "Digest:", digest, x.digest
    print "done. closing conn."
    conn.notify.stop()
    conn.close()
    

print "Testing server/client . . ."
s = bjsonrpc.createserver(handler_factory=MyHandler, port = RPC_PORT, host = "0.0.0.0")
s.debug_socket(True)
threading.Thread(target=thread1).start()
s.serve()




