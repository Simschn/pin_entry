import subprocess
import serial
import os
import re
import threading, time
import matplotlib.pyplot as plt
 

cmd = ['sigrok-cli','-d','fx2lafw',
       '-C','D5,D7',
       '-c','samplerate=12m',
       '-w',
       '-t','D7=f',
       '--time','3000',
       '-P','timing:data=D5',
       '-P','timing:data=D7',
       '-A','timing=time'] # sigrok-cli command to be used
#cmduart = ['sigrok-cli',
#           '-d','fx2lafw',
#           '-C','D5,D7',
#           '-c','samplerate=6m'
#           ,'--time' ,'10000'
#           ,'-P','uart:rx=D5:tx=D7:baudrate=9600:format=hex'
#           ,'-A','uart=rx-packet']# sigrok-cli command to be used
print(' '.join(cmd))
p = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE)
#ttyUSB = open('/dev/ttyUSB0','w')
ser = serial.Serial('/dev/ttyUSB0')
for i in range(3):

#4208154711a
    ser.write(b'0000000000a')
    ser.flush()
#    ser.flush()
    time.sleep(1)
#    ttyUSB.write('11234567890')
#    ttyUSB.flush()

ser.close()

sout = p.communicate()[0]
print(repr(sout))
time.sleep(3)
timingdata = repr(sout).replace('\\n','\n').splitlines()
tdata_lines = [] 
# map(lambda timingdata: Timing(timingdata.find('timing-1'))
# ([0-9.]+) [^\(]+([0-9.]+)
class Timing:
    def __init__(self,i,grp,ns):
        self.i = i
        self.grp = grp
        self.ns = ns 
def toTiming(string):
    i = re.search('([0-9]+)', string)
    grp = re.search('timing-([0-9])', string)
    ns = re.search('([0-9]+\.[0-9]+)', string)
    if(i and grp and ns):
        return Timing(i.group(1),grp.group(1),ns.group(1)) 
    else:
        return None

for i in range(len(timingdata)):
    tdata_lines.append('{} {}'.format(i, timingdata[i]))
print(tdata_lines)
samples = []
for i in range(len(tdata_lines)):
    samples.append(toTiming(tdata_lines[i]))

x = []
y = [] 
nsagg = 0
for i in range(len(samples)):
    if samples[i]:
       #print('{}i {}grp {}ns'.format(samples[i].i, samples[i].grp, samples[i].ns))
        nsagg += float(samples[i].ns)
        y.append(samples[i].grp)
        x.append(nsagg)
# x axis values 
# corresponding y axis values 
  
# plotting the points  
plt.plot(x, y) 
  
# naming the x axis 
plt.xlabel('x - axis') 
# naming the y axis 
plt.ylabel('y - axis') 
  
# giving a title to my graph 
plt.title('My first graph!') 
  
# function to show the plot 
plt.show()
#timingRx = re.search(r'timing-1',timingdata)
#timingTx = re.search(r'timing-2',timingdata)
#print(tdata_lines)
#print(timingRx)
#print(timingTx)


#uart = repr(sout)
#output = repr(sout).replace('\\n','\n')
#print(uart)
#uart = uart.
