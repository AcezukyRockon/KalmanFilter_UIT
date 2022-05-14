# import OS module
import os
from pydub import AudioSegment
 
# Get the list of all files and directories
path = "D://1.study//doannhung//baocao//tuan12//dataset_vn//trai"
dir_list = os.listdir(path)
 
print("Files and directories in '", path, "' :")
 
# prints all files
print(dir_list)
print("length dir: ",len(dir_list))

for i in range(len(dir_list)):
    print(dir_list[i])
    
    #importing file from location by giving its path
    sound = AudioSegment.from_wav("D://1.study//doannhung//baocao//tuan12//dataset_vn//trai//"+dir_list[i])
    sound = sound.set_channels(1)

    #Selecting Portion we want to cut
    StrtMin = 0
    StrtSec = 0

    EndMin = 0
    EndSec = 1

    # Time to milliseconds conversion
    StrtTime = StrtMin*60*1000+StrtSec*1000
    EndTime = StrtMin*60*1000+EndSec*1000

    # Opening file and extracting portion of it
    extract = sound[StrtTime:EndTime]

    # Saving file in required location
    extract.export("D://1.study//doannhung//baocao//tuan12//dataset_vn_new//trai//"+dir_list[i], format="wav")

    # new file portion.mp3 is saved at required location