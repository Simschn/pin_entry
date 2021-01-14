import subprocess
import os
 

cmd = ['sigrok-cli','-d','fx2lafw',
       '-C','D5,D7',
       '-c','samplerate=6m',
       '--time','3000',
       '-P','timing:data=D5',
       '-P','timing:data=D7',
       '-A','timing=time'] # sigrok-cli command to be used
cmduart = ['sigrok-cli',
           '-d','fx2lafw',
           '-C','D5,D7',
           '-c','samplerate=6m'
           ,'--time' ,'3000'
           ,'-P','uart:rx=D5:tx=D7:baudrate=9600:format=hex'
           ,'-A','uart=rx-packet']# sigrok-cli command to be used
print(' '.join(cmd))
p = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE)
ttyUSB = open('/dev/ttyUSB0','w')
ttyUSB.write('11234567890')
ttyUSB.flush()
sout = p.communicate()[0]
timing = repr(sout).replace('\\n','\n')

print(timing)


#uart = repr(sout)
#output = repr(sout).replace('\\n','\n')
#print(uart)
#uart = uart.
