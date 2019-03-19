''' footsteps.py

  To compile:
  python3 footsteps.py -lopenal

  Requires data "footsteps.raw", which is any signed-16bit
  mono audio data (no header!); assumed sample rate is 44.1kHz.

 '''

import os
import sys
import time
import math
import gc
import random
from ctypes import *

''' magnetometer model header '''
import py_qmc5883l

''' OpenAL headers '''
from openal import *
from openal.alc import *

''' Load a file into memory, returning the buffer and
    setting bufsize to the size-in-bytes '''
def load (fname):
    buffer = open(fname, 'rb').read()
    return buffer

def rect(polar):
    r = polar[0]
    theta = polar[1]
    return [r*math.sin(theta), 1.5, r*math.cos(theta)]

''' Defining the main function on Python '''
def main():

  ''' Defining a variable to name all the functions of the magnetometer '''
  sensor = py_qmc5883l.QMC5883L()

  ''' current position and where to walk to... start just 1m ahead '''
  target_polar = [5.0, 0.0]
  curr = targ = rect(target_polar)

  ''' initialize OpenAL context, asking for 44.1kHz to match HRIR data '''
  contextAttr = [ALC_FREQUENCY,44100,0]
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
  alGenSources( 4, cast(source, POINTER(ctypes.c_uint)) );

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
  alGenBuffers( 4, cast(buffer, POINTER(ctypes.c_uint)) );

  data = load ( 'nord.raw' )
  data2 = load( 'sud.raw' )
  data3 = load ( 'est.raw' )
  data4 = load( 'oest.raw' )

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
  dt = 1./60.
  vel = 0.8 * dt

  ''' BEGIN! '''
  alSourcePlay( source[0] );
  time.sleep(2)
  alSourcePlay( source[1] );
  time.sleep(2)
  alSourcePlay( source[2] );
  time.sleep(2)
  alSourcePlay( source[3] );
  time.sleep(2)

  ''' loop forever... walking to random, adjacent, integer coordinates '''
  while(True):

    ''' Initial position of the x,y,z coordinates of the sound 
    relating to the current positions 'curr' and the target 'targ' one '''

    rho = round(sensor.get_bearing2(), 4)

    print(rho)

    target_polar[1] = 180 + rho #Coordenada NORD
    target_polar[1] = 90 + rho #Coordenada EST
    target_polar[1] = rho #Coordenada SUD
    target_polar[1] = -90 + rho #Coordenada OEST

    if target_polar[1] > 360.0:
        target_polar[1] = target_polar[1] - 360.0
    if target_polar[1] < 0.0:
        target_polar[1] = target_polar[1] + 360.0

    target_polar[1] = target_polar[1] * math.pi /180.0
#    print(target_polar[1])

    targ = rect(target_polar)

#    print(targ)

    alSource3f( source[0], AL_POSITION, targ[0], targ[1], targ[2] )
    alSource3f( source[0], AL_VELOCITY, 0.0, 0.0, 0.0 )
    #print(curr, targ)
    time.sleep( (int)(1*dt) )

    alSource3f( source[1], AL_POSITION, targ[0], targ[1], targ[2] )
    alSource3f( source[1], AL_VELOCITY, 0.0, 0.0, 0.0 )
    #print(curr, targ)
    time.sleep( (int)(1*dt) )


  ''' cleanup that should be done when you have a proper exit... ;) '''
  alDeleteSources( 1, ctypes.pointer(source) )
  alDeleteBuffers( 1, ctypes.pointer(buffer ) )
  alcDestroyContext( context )
  alcCloseDevice( device )

  return


if __name__ == '__main__':
	main()

