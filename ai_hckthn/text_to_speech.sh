# Script based on Pico Text to Speech found in https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis):
#Requires sudo apt-get install libttspico-utils

# Usage:
  #In terminal run:
    # bash speak.sh "Hello Dude" 
  # In python3 run: 
    # os.system('bash speak.sh "{}"'.format(SomeText))
text=$1
pico2wave -w temporary.wav "$text" && aplay temporary.wav
