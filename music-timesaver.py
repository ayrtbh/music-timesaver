import subprocess
from time import gmtime, strftime
import os


original_audio_path = input("drag audio file here:\n")


subprocess.call("mkdir LR_mix_pool", shell=True)

subprocess.call("python3 timesaver_L.py '{}'".format(original_audio_path), shell = True)
subprocess.call("python3 timesaver_R.py '{}'".format(original_audio_path), shell = True)

# final_name = strftime("%Y_%m_%d_%H_%M_%S", gmtime())

final_name = os.path.basename(original_audio_path)

subprocess.call("sox -M LR_mix_pool/*.wav '{}_in_half_time'.wav".format(final_name), shell = True)

subprocess.call("rm -r LR_mix_pool", shell=True)
