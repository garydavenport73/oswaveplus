#   Gary Davenport, CLI player functions 6/8/2021
#
#   plays wav files using native wav playing command line interface calls
#   for Windows 10, Linux, and MacOS
#
#   Windows10 uses the Media.Soundplayer module built into Windows 10
#       and winsound modulee part of Python standard library
#   Linux uses ALSA which is part of the Linux kernel since version 2.6 and later
#   MacOS uses the afplay module which is present OS X 10.5 and later
#   

from platform import system
import subprocess
from subprocess import Popen, PIPE
import os
from threading import Thread
from time import sleep
import sndhdr
from random import random
if system()=="Windows":
    import winsound

class LinuxOrMacOSPlayerMusicLooper:
    def __init__(self, fileName):
        self.fileName = fileName
        self.playing = False
        self.songProcess = None

    def _playwave(self):
        self.songProcess=playwave(self.fileName)

    def _playloop(self):
        while self.playing==True:
            self.songProcess=playwave(self.fileName)
            sleep(self.getWavDurationFromFile(self.fileName))

    def startMusicLoopWave(self):
        if self.playing==True:
            print("Already playing, stop before starting new.")
            return
        else:
            self.playing=True
            t = Thread(target=self._playloop)
            t.setDaemon(True)
            t.start()
            
    def stopMusicLoop(self):
        if self.playing==False:
            print(str(self.songProcess)+" already stopped, play before trying to stop.")
            return
        else:
            self.playing=False
            stopwave(self.songProcess)

    def getSongProcess(self):
        return(self.songProcess)

    def getIsPlaying(self):
        return(self.playing)

    def getWavDurationFromFile(self,filename):
        frames = sndhdr.what(filename)[3]
        rate = sndhdr.what(filename)[1]
        duration = float(frames)/rate
        return duration

class WinSoundWavePlayer:
    def __init__(self):
        self.winsoundName=""
        self.winsoundInUse=False
        self.filename=""

    def _setWinsoundInUseToFalseAfterSeconds(self):
        #print("setting winsound in use ", self.winsoundName,"to False in ",self.duration,"seconds")
        sleep(self.duration)
        print("duration",self.duration,"over on ", self.winsoundName)
        self.winsoundInUse=False
        self.winsoundName=""
    
    def _playWithPythonWinSoundModule(self,filename, block):
        #get duration of wavefile
        self.duration=self.getWavDurationFromFile(filename)
        #make an unique alias
        self.winsoundName="sound"+str(random())
        #set winsound to being used
        self.winsoundInUse=True
        #play the sound
        winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
        #flip winsoundInUse and name="" after sound over
        t=Thread(target=self._setWinsoundInUseToFalseAfterSeconds)
        t.daemon=True
        t.start()
        if block==True: t.join()

    def _playUsingPowershell(self,filename, block):
        command="%SystemRoot%\system32\WindowsPowerShell/v1.0\powershell.exe -c (New-Object Media.SoundPlayer '"+os.path.abspath(filename)+"').PlaySync()"
        if block==True: P = subprocess.Popen(command, universal_newlines=True, shell=True,stdout=PIPE, stderr=PIPE).communicate()
        else: P = subprocess.Popen(command, universal_newlines=True, shell=True,stdout=PIPE, stderr=PIPE)
        return P

    def playwave(self,filename, block=False):
        if self.winsoundInUse==False: #winsound python module not used, use it
            print("playing with winsound python")
            self._playWithPythonWinSoundModule(filename, block)
            return self.winsoundName
        else: #winsound python module being used, use alt method
            #issue command line argument to play sound
            #return the process
            print(self.winsoundName,"in use, use alt method")
            return self._playUsingPowershell(filename, block)

    def stopwave(self, song):
        #stopping direct winsound python method
        if self.winsoundInUse==True and str(song)==self.winsoundName:
            winsound.PlaySound(None,winsound.SND_FILENAME)
            self.winsoundInUse==False
            self.winsoundName=""
        #stopping a subprocess call
        elif type(song)!=str and song is not None:
            #print(type(song))
            #print("put method here to stop the sound")
            try:
                #song.terminate()
                #song.kill()
                #command="taskkill /F /T /PID "+ str(song.pid) + " >NUL"
                #sp=subprocess.Popen(command, universal_newlines=True, shell=True,stdout=PIPE, stderr=PIPE)
                os.system("taskkill /F /T /PID "+ str(song.pid) + " >NUL") 
            except:
                print("caught stopwave with pid",str(song.pid))
    # put subprocess call to loop wave here and return it
    def loopwave(self, filename, numberOfLoops = 999999):
        totalLength=min(self.getWavDurationFromFile(filename)*numberOfLoops, 999999)
        #t=Thread(target=winsound.PlaySound, args=[filename, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC]).start()
        command="%SystemRoot%\system32\WindowsPowerShell/v1.0\powershell.exe -c (New-Object Media.SoundPlayer '"+os.path.abspath(filename)+"').PlayLooping();Start-Sleep -s "+ str(totalLength)
        #command="%SystemRoot%\system32\WindowsPowerShell/v1.0\powershell.exe -c while($true){(New-Object Media.SoundPlayer '"+os.path.abspath(filename)+"').PlaySync()}"
        print(command)
        P = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=PIPE, stderr=PIPE)
        print(P)
        return P

    # terminate the subprocess
    def stoploop(self, loop):
        self.stopwave(loop)

    def iswaveplaying(self,song):
        #print(song)
        if song is None: return False
        #print("not a string", type(song)!=str, "song is not None", song is not None)
        #if it is a direct python method
        elif self.winsoundInUse==True and str(song)==self.winsoundName:
            return True
        #check to see if process is active here
        elif type(song)!=str and song is not None:
            #print("put method here to see if process is running")
            playing = song.poll() is None
            return playing
        else:
            return False
        
    def isloopplaying(self,loop):
        #print("put code here to see if loop subprocess is active")
        return self.iswaveplaying(loop)

    def getWavDurationFromFile(self,filename):
        frames = sndhdr.what(filename)[3]
        rate = sndhdr.what(filename)[1]
        duration = float(frames)/rate
        return duration

class LinuxOrMacOSPlayer:
    def __init__(self):
        pass
    def playwave(self,fileName, block=False):
        if system()=="Linux": command = "exec aplay --quiet " + os.path.abspath(fileName)
        elif system()=="Darwin": command = "exec afplay \'" + os.path.abspath(fileName)+"\'"
        if block==True: P = subprocess.Popen(command, universal_newlines=True, shell=True,stdout=PIPE, stderr=PIPE).communicate()
        else: P = subprocess.Popen(command, universal_newlines=True, shell=True,stdout=PIPE, stderr=PIPE)
        return P

    def stopwave(self,process):
        if process is None: return
        else: process.terminate()

    def getIsPlaying(self,process):
        isSongPlaying=False
        if process is not None:
            try: return(process.poll() is None)
            except: pass
        return isSongPlaying

    def playsound(self,fileName, block=True):
        return(playwave(fileName, block))

    def loopwave(self,fileName):
        looper=LinuxOrMacOSPlayerMusicLooper(fileName)
        looper.startMusicLoopWave()
        return(looper)

    def stoploop(self,looperObject):
        if looperObject is None: return
        else: looperObject.stopMusicLoop()

    def getIsLoopPlaying(self,looperObject):
        if looperObject is None: return False
        else: return(looperObject.getIsPlaying())

    def getWavDurationFromFile(self,filename):
        frames = sndhdr.what(filename)[3]
        rate = sndhdr.what(filename)[1]
        duration = float(frames)/rate
        return duration

if system()=="Windows":
    myWinPlayer=WinSoundWavePlayer()
    playwave=myWinPlayer.playwave
    stopwave=myWinPlayer.stopwave
    loopwave=myWinPlayer.loopwave
    stoploop=myWinPlayer.stoploop
    getIsPlaying=myWinPlayer.iswaveplaying
    getIsLoopPlaying=myWinPlayer.isloopplaying

elif system()=="Linux" or system()=="Darwin":
    playwave=LinuxOrMacOSPlayer().playwave
    stopwave=LinuxOrMacOSPlayer().stopwave
    loopwave=LinuxOrMacOSPlayer().loopwave
    stoploop=LinuxOrMacOSPlayer().stoploop
    getIsPlaying=LinuxOrMacOSPlayer().getIsPlaying
    getIsLoopPlaying=LinuxOrMacOSPlayer().getIsLoopPlaying