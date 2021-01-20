#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import serial
import os
import re
import threading, time
 
#globals
testruns = 2

cmd = ['sigrok-cli',
           '-d','fx2lafw',
           '-c','samplerate=24m',
           '--continuous',
           '-C','D5,D7',
           '-P','uart:rx=D5:tx=D7:baudrate=57600:format=ascii',
           '-A', 'uart=rx-data:tx-data',
           '--protocol-decoder-samplenum']# sigrok-cli command to be used
print(' '.join(cmd))


def collectSamples(payload):
    ser = serial.Serial('/dev/ttyUSB0', baudrate=57600)
    sigrok = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stdin=subprocess.PIPE,
                     universal_newlines=True)
    # secret arduino handshake
    ser.write(bytes(payload + '\n','ascii'))
    time.sleep(0.3)
    for i in range(testruns):
        for j in range(len(payload)):
            ser.write(bytes(payload[j],'ascii'))
            #print(bytes(payload,'ascii')[j])
            ser.flush()
            time.sleep(0.0001)  #magic number no questions asked
        ser.write(bytes('\n','ascii')) #print extra char to finish pin sequence
        time.sleep(0.08) #magic number no questions asked
    ser.close()
    sigrok.kill() #hard flush
    time.sleep(1)
    samples = []
    for line in iter(sigrok.stdout.readline, ''): 
        samples.append(line.replace('\n',''))
    return samples


#sample layout: 745970-755970 uart-1: 1
class SampleList:
    def __init__(self,samples):
        self.samples = samples
        self.counter = 0
    
    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        self.counter += 1 
        if (self.counter >= len(self.samples)):
           raise StopIteration 
        timedifference = int(self.samples[self.counter].start[0]) - int(self.samples[self.counter-1].end[0])
        char = self.samples[self.counter].char[0]
        lastchar = self.samples[self.counter-1].char[0]
        return timedifference, lastchar, char

    
class Sample:
    def __init__(self,sample_nr_start,sample_nr_end,char):
        self.start = sample_nr_start
        self.end = sample_nr_end
        self.char = char

    def toString(self):
        return 'start: {} end: {} char: {}'.format(self.start[0], self.end[0], self.char[0]);

def parseSample(sample):
    sample_nr_start = re.search('([0-9]+)', sample).groups(1)
    sample_nr_end = re.search('-([0-9]+)', sample).groups(1)
    char = re.search('(.)$',sample).groups(1)
    return Sample(sample_nr_start, sample_nr_end, char)

def filterValidSamples(samples):
    validSamples = []
    return validSamples

def average(payload):
    samples = collectSamples(payload)
    samples_objs = list(map(parseSample,samples))
    #print(len(samples_objs))
    samplelist = SampleList(samples_objs)
    average = 0
    bbcounter = 0
    for d, lc, c in samplelist:
        if lc == ']' and c == ']':
            average += d
            bbcounter += 1
    #         print('{} --{}-> {}'.format(lc,d,c))
    print('payload: {} average: {}'.format(payload ,average / bbcounter))
    return average/bbcounter
    
pin = '0000000000'
happylittlenumbers ='0123456789'

for i in range(len(pin)):
    averages = []
    for num in happylittlenumbers:
        prenum = pin[:i]
        postnum = pin[i+1:]
        pin = prenum+num+postnum
        averages.append(average(pin))
    bestAvg = max(averages) 
    index = averages.index(bestAvg)
    pre = pin[:i]
    test = happylittlenumbers[index]
    post = pin[i+1:]
    pin = pre + test + post

print('Secret: {}'.format(pin))
