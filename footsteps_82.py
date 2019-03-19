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
import re
import ctypes

''' gps module import '''
from neo6 import GpsNeo6

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

  ''' Defining a variable to name all the functions of the gps '''
  gps=GpsNeo6(port="/dev/ttyAMA0",debit=9600,diff=2) #diff is difference betw$

  lat_FGC = 41.56344849685262
  long_FGC = 2.0190451151906927

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
  source = c_uint(0)
  alGenSources( 1, source );

  alSourcef( source, AL_PITCH, 1. )
  alSourcef( source, AL_GAIN, 1. )
  alSource3f( source, AL_POSITION, curr[0], curr[1], curr[2] )
  alSource3f( source, AL_VELOCITY, 0.,0.,0. )
  alSourcei( source, AL_LOOPING, AL_TRUE )

  ''' allocate an OpenAL buffer and fill it with monaural sample data '''
  buffer = ctypes.c_uint(0)
  alGenBuffers( 1, ctypes.pointer(buffer));

  data = load ( 'nord.raw' )

  dataSize = ctypes.c_int( len (data) )

  # for simplicity, assume raw file is signed-16b at 44.1kHz
  alBufferData( buffer, AL_FORMAT_MONO16, data, dataSize, 44100 )

  gc.collect( )

  alSourcei( source, AL_BUFFER, buffer.value )

  ''' state initializations for the upcoming loop '''
  random.seed( );
  dt = 1./60.
  vel = 0.8 * dt

  ''' BEGIN! '''
  alSourcePlay( source );

  ''' loop forever... walking to random, adjacent, integer coordinates '''
  while(True):

      ''' Initial position of the x,y,z coordinates of the sound
      relating to the current positions 'curr' and the target 'targ' one '''

      gps.traite()

      print(gps.time,gps.latitude,gps.longitude,gps.satellite)

      lat_orig = gps.latitude
      long_orig = gps.longitude

      target_polar[1] = lat_orig - lat_FGC  #Diferencia Latitud
      target_polar[1] = long_orig - long_FGC #Diferencia Longitud

      if target_polar[1] > 360.0:
          target_polar[1] = target_polar[1] - 360.0
      if target_polar[1] < 0.0:
          target_polar[1] = target_polar[1] + 360.0

      target_polar[1] = target_polar[1] * math.pi /180.0

      targ = rect(target_polar)

      alSource3f( source[0], AL_POSITION, targ[0], targ[1], targ[2] )
      alSource3f( source[0], AL_VELOCITY, 0.0, 0.0, 0.0 )
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

