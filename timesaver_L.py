import os
import subprocess
from time import gmtime, strftime
import sys

# fragment length in samples
fragment_len = 44100

# get the audio file path
# original_audio_path = input("drag audio file here:\n")
original_audio_path = sys.argv[1]
# get the audio file path

# make a tmp folder for sox processing
tmp_path = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
subprocess.call("mkdir {}".format(tmp_path), shell=True)
# make a tmp folder for sox processing

# split the original audio to parts and put them in the tmp folder
subprocess.call("sox {} {}/%1n.wav trim 0 {}s : newfile : restart".format(original_audio_path, tmp_path, fragment_len), shell=True)
# split the original audio to parts and put them in the tmp folder


cmd = "ls {} | wc -l".format(tmp_path)
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
how_many_files_in_this_folder = p.stdout.read().strip()

fn = int(how_many_files_in_this_folder)
print(fn)

# make the input file list (a reverse list)
fl = []
for i in range(fn):
	fl.append("{}/{}.wav".format(tmp_path,i+1))
# fl.reverse()
fl = fl[::2] # this only get the even fragments
# print(fl)
# make the input file list (a reverse list)

# because sox can not handle more than 200 open files

# the tricky parts: split the long list to multiple lists
def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs
list_of_lists = split(fl, 150)
# print(list_of_lists)
# the tricky parts: split the long list to multiple lists

# make many mixs and chain them together
n = 0
subprocess.call("mkdir mix_list", shell=True)

for l in list_of_lists:
	n += 1
	filelist = " ".join(l)
	subprocess.call("sox {} mix_list/{}_mix_{}.wav".format(filelist, tmp_path, n), shell=True)

subprocess.call("sox mix_list/*.wav -c 1 LR_mix_pool/{}_mix_L.wav".format(tmp_path), shell=True)
# make many mixs and chain them together


# remove the tmp folder and its contents
subprocess.call("rm -r {}".format(tmp_path),shell=True)
subprocess.call("rm -r mix_list", shell=True)
# remove the tmp folder and its contents