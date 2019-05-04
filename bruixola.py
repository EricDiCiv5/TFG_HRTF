

''' Load a file into memory, returning the buffer and
    setting bufsize to the size-in-bytes '''
def load (fname):
    buffer = open(fname, 'rb').read()
    return buffer

def rect(polar):
    r = polar[0]
    theta = polar[1]
    return [r*math.sin(theta), 1.5, r*math.cos(theta)]

def bruixola():
    global estat, MUTE

    sound_dir = '/home/pi/sounds'

    ''' Defining a variable to name all the functions of the magnetometer '''
    sensor = py_qmc5883l.QMC5883L()

    ''' current position and where to walk to... start just 1m ahead '''
    target_polar = [5.0, 0.0]
    curr = targ = rect(target_polar)

    ''' initialize OpenAL context, asking for 44.1kHz to match HRIR data '''
    contextAttr = [ALC_FREQUENCY,44100,0,ALC_MONO_SOURCES,4]
    device = alcOpenDevice( None )
    context = alcCreateContext( device, (ctypes.c_int * len(contextAttr))(*contextAttr) )
    alcMakeContextCurrent( context )

    ''' listener at origin, facing down -z (ears at 1.5m height) '''
    alListener3f( AL_POSITION, 0., 1.5, 0. )
    alListener3f( AL_VELOCITY, 0., 0., 0. )
    orient = [0.0, 0.0, -1.0, 0.0, 1.0, 0.0]
    alListenerfv( AL_ORIENTATION, (ctypes.c_float * len(orient))(*orient) )

    ''' this will be the source of ghostly footsteps... '''
    source = (ctypes.c_uint * 4)(0,0)
    alGenSources( 4, ctypes.cast(source, POINTER(c_uint)) );

    print(device)
    try:
        device
    except NameError:
        print("device is not set up with value" , device)

    print(context)
    try:
        context
    except NameError:
        print("context is not set up with value" , context)

    alSourcef( source[0], AL_PITCH, 1. )
    alSourcef( source[0], AL_GAIN, 1. )
    alSource3f( source[0], AL_POSITION, curr[0], curr[1], curr[2] )
    alSource3f( source[0], AL_VELOCITY, 0.,0.,0. )
    alSourcei( source[0], AL_LOOPING, AL_TRUE )

    alSourcef( source[1], AL_PITCH, 1. )
    alSourcef( source[1], AL_GAIN, 1. )
    alSource3f( source[1], AL_POSITION, curr[0], curr[1], curr[2] )
    alSource3f( source[1], AL_VELOCITY, 0.,0.,0. )
    alSourcei( source[1], AL_LOOPING, AL_TRUE )

    alSourcef( source[2], AL_PITCH, 1. )
    alSourcef( source[2], AL_GAIN, 1. )
    alSource3f( source[2], AL_POSITION, curr[0], curr[1], curr[2] )
    alSource3f( source[2], AL_VELOCITY, 0.,0.,0. )
    alSourcei( source[2], AL_LOOPING, AL_TRUE )

    alSourcef( source[3], AL_PITCH, 1. )
    alSourcef( source[3], AL_GAIN, 1. )
    alSource3f( source[3], AL_POSITION, curr[0], curr[1], curr[2] )
    alSource3f( source[3], AL_VELOCITY, 0.,0.,0. )
    alSourcei( source[3], AL_LOOPING, AL_TRUE )

    ''' allocate an OpenAL buffer and fill it with monaural sample data '''
    buffer = (ctypes.c_uint * 4)(0,0)
    alGenBuffers( 4, cast(buffer, POINTER(c_uint)) );

    print(device)
    try:
        device
    except NameError:
        print("device is not set up with value" , device)

    print(context)
    try:
        context
    except NameError:
        print("context is not set up with value" , context)


    data = load(join(sound_dir, 'nord.raw' ))
    data2 = load(join(sound_dir, 'sud.raw' ))
    data3 = load(join(sound_dir, 'est.raw' ))
    data4 = load(join(sound_dir, 'oest.raw' ))

    dataSize = ctypes.c_int( len (data) )
    dataSize2 = ctypes.c_int( len (data2) )
    dataSize3 = ctypes.c_int( len (data3) )
    dataSize4 = ctypes.c_int( len (data4) )

    # for simplicity, assume raw file is signed-16b at 44.1kHz
    alBufferData( buffer[0], AL_FORMAT_MONO16, data, dataSize, 44100 )
    gc.collect( )

    alBufferData( buffer[1], AL_FORMAT_MONO16, data2, dataSize2, 44100 )
    gc.collect( )

    alBufferData( buffer[2], AL_FORMAT_MONO16, data3, dataSize3, 44100 )
    gc.collect( )

    alBufferData( buffer[3], AL_FORMAT_MONO16, data4, dataSize4, 44100 )
    gc.collect( )

    alSourcei( source[0], AL_BUFFER, buffer[0] )
    alSourcei( source[1], AL_BUFFER, buffer[1] )
    alSourcei( source[2], AL_BUFFER, buffer[2] )
    alSourcei( source[3], AL_BUFFER, buffer[3] )

    ''' state initializations for the upcoming loop '''
    random.seed( );

    ''' BEGIN! '''
    Src = 0

    ''' loop forever... walking to random, adjacent, integer coordinates '''
    while(True):

      rho = round(sensor.get_bearing2(), 4)

      print(rho)

      if GPIO.event_detected(12):
          print("Acabant bruixola...")
#####
#
# S'ha d'arreglar per sortir ordenadament
#
#####
#          alDeleteSources( 1, ctypes.pointer(source)*4)
#          alDeleteBuffers( 1, ctypes.pointer(buffer)*4)

           #alDeleteSources( 4, cast(source, POINTER(c_uint)) );
           #alDeleteSources( 4, cast(buffer, POINTER(c_uint)) );


           #alDeleteSources( 4, byref(c_uint(source)) )
           #alDeleteBuffers( 4, byref(c_uint(buffer)) )


           #alDeleteSources( 4, pointer(c_uint(source)) )
           #alDeleteBuffers( 4, pointer(c_uint(buffer)) )


           #alDeleteSources( 1, cast(source, POINTER(c_uint)) );
           #alDeleteSources( 1, cast(buffer, POINTER(c_uint)) );


           #alDeleteSources( 1, pointer(c_ulong(source[0])))
           #alDeleteBuffers( 1, pointer(c_ulong(buffer[0])))

           #alDeleteSources( 1, pointer(c_ulong(source[1])))
           #alDeleteBuffers( 1, pointer(c_ulong(buffer[1])))

           #alDeleteSources( 1, pointer(c_ulong(source[2])))
           #alDeleteBuffers( 1, pointer(c_ulong(buffer[2])))

           #alDeleteSources( 1, pointer(c_ulong(source[3])))
           #alDeleteBuffers( 1, pointer(c_ulong(buffer[3])))


           #alDeleteSources(4, pointer(source)[0])
           #alDeleteBuffers(4, pointer(buffer)[0])

           #alDeleteSources(4, pointer(source)[1])
           #alDeleteBuffers(4, pointer(buffer)[1])

           #alDeleteSources(4, pointer(source)[2])
           #alDeleteBuffers(4, pointer(buffer)[2])

           #alDeleteSources(4, pointer(source)[3])
           #alDeleteBuffers(4, pointer(buffer)[3])


           #alDeleteSources(4, pointer(cast(source, POINTER(c_uint))))
           #alDeleteSources(4, pointer(cast(buffer, POINTER(c_uint))))

           #alDeleteSources(4, int(source))
           #alDeleteBuffers(4, int(buffer))


#          alcDestroyContext( context )
#          alcCloseDevice( device )
          return MUTE

      if Src == 0:

        alSourcePlay( source[0] );
        time.sleep(1)
        alSourceStop( source[0] );

        target_polar[1] = 180 + rho #Coordenada NORD

        if target_polar[1] > 360.0:
          target_polar[1] = target_polar[1] - 360.0
        if target_polar[1] < 0.0:
          target_polar[1] = target_polar[1] + 360.0

        target_polar[1] = target_polar[1] * math.pi /180.0
    #   print(target_polar[1])

        targ = rect(target_polar)

        alSource3f( source[0], AL_POSITION, targ[0], targ[1], targ[2] )
        alSource3f( source[0], AL_VELOCITY, 0.0, 0.0, 0.0 )
        #time.sleep(1)

      if Src == 1:

        alSourcePlay( source[1] );
        time.sleep(1)
        alSourceStop( source[1] );

        target_polar[1] = rho #Coordenada SUD

        #Adjusting the boundaries of the trigonometric circle for the first coord$
        if target_polar[1] > 360.0:
          target_polar[1] = target_polar[1] - 360.0
        if target_polar[1] < 0.0:
          target_polar[1] = target_polar[1] + 360.0

        target_polar[1] = target_polar[1] * math.pi /180.0
   #    print(target_polar[1])

        targ = rect(target_polar)

        alSource3f( source[1], AL_POSITION, targ[0], targ[1], targ[2] )
        alSource3f( source[1], AL_VELOCITY, 0.0, 0.0, 0.0 )
        #time.sleep(1)

      if Src == 2:

        alSourcePlay( source[2] );
        time.sleep(1)
        alSourceStop( source[2] );

        target_polar[1] = 90 + rho #Coordenada EST

        #Adjusting the boundaries of the trigonometric circle for the first coord$
        if target_polar[1] > 360.0:
          target_polar[1] = target_polar[1] - 360.0
        if target_polar[1] < 0.0:
          target_polar[1] = target_polar[1] + 360.0

        target_polar[1] = target_polar[1] * math.pi /180.0
   #    print(target_polar[1])

        targ = rect(target_polar)

        alSource3f( source[2], AL_POSITION, targ[0], targ[1], targ[2] )
        alSource3f( source[2], AL_VELOCITY, 0.0, 0.0, 0.0 )
        #time.sleep(1)

      if Src == 3:

        alSourcePlay( source[3] );
        time.sleep(1)
        alSourceStop( source[3] );

        target_polar[1] = -90 + rho #Coordenada OEST

        #Adjusting the boundaries of the trigonometric circle for the first coord$
        if target_polar[1] > 360.0:
          target_polar[1] = target_polar[1] - 360.0
        if target_polar[1] < 0.0:
          target_polar[1] = target_polar[1] + 360.0

        target_polar[1] = target_polar[1] * math.pi /180.0
    #    print(target_polar[1])

        targ = rect(target_polar)

        alSource3f( source[3], AL_POSITION, targ[0], targ[1], targ[2] )
        alSource3f( source[3], AL_VELOCITY, 0.0, 0.0, 0.0 )
        #time.sleep(1)

        Src = -1

      Src += 1

import os
import sys
import time
import math
import gc
import random

from ctypes import *
from os.path import join

import RPi.GPIO as GPIO

from openal import *
from openal.alc import *

import py_qmc5883l

estat = 2
MUTE = 0

if __name__ == '__main__':

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(12,GPIO.RISING, bouncetime = 1)

        estat = bruixola() # Displays bruixola

        print('Acabant execucio independent', estat)

