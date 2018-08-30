#### Filetransfer.py is used to transfer files between two Agave systems and compute, the transfer time using Agave Files API calls
#### File transfer is done between two Agave storage systems, which may have different underlying hosts but are registered with same tenant
#### This script requires following command line arguments
#### arg 1 : Base url for the tenant
#### arg 2:  Authorization token
#### arg 3:  Absolute path of the file to store response time log
#### arg 4:  Agave storage system name from where file transfer will initiate (source), we call it AGAVE_SOURCE_SYSTEM
#### arg 5:  Agave storage system where file will be transfered (destination), we call it AGAVE_DESTINATION_SYSTEM
### Run as : run Filetransfer.py $Base_url $Token $LofFilePath $AgaveSourceSystemName $AgaveDestinationSystemName
#### You will need to install Agave py. Installation details can be found at https://github.com/TACC/agavepy/blob/master/README.rst
import sys
import json
from agavepy.agave import Agave
from agavepy.async import AgaveAsyncResponse
import time

#########Set up variables#####################
# Base url of the tenant
URL = sys.argv[1]
# Authorization token
TOKEN = sys.argv[2]

# FILE_SOURCE contains the relative path for test file on the source system to be transfered
FILE_SOURCE = '/Path/SourceFile.txt'

# FILE_DEST is the name of the file on the destination system after transfer, you may choose any name
FILE_DEST = 'DestinationFile.txt'

# Transfer time log will be stored
TRANSFER_TIME = sys.argv[3]

# Agave source system from where file transfer will be initiated
AGAVE_SOURCE_SYSTEM = sys.argv[4]

# Agave destination system where file to be transfered 
AGAVE_DESTINATION_SYSTEM = sys.argv[5]

# Url to Ingest is needed for agave files import data call
URL_TO_INGEST='agave://'+AGAVE_SOURCE_SYSTEM+ FILE_SOURCE

######## Make Agave connection #######################

ag = Agave(api_server=URL, token=TOKEN)

############## Before initiating file transfer ###########################
### Before we initiate file transfer, we make sure that the test file is uploaded to the source system
### We use Agave file upload call to upload the file to the source system
### If the test file is already present this call can be skipped and this block can be commented
#filePath: The path of the file relative to the user’s default storage location. (string)
# More details can be found on AgavePy readthedocs
# https://agavepy.readthedocs.io/en/latest/agavepy.files.html#importdata-import-a-file-via-direct-upload-or-importing-from-a-url-to-the-user-s-default-storage-location
FILE_UPLOAD= ag.files.importData(systemId=AGAVE_SOURCE_SYSTEM,
                                 filePath='/Path where you want to upload file source system',
                                 fileToUpload=open('AbsolutePath/local/SourceFile.txt', 'rb'))
arsp = AgaveAsyncResponse(ag, FILE_UPLOAD)
status = arsp.result(timeout=120)
print(status)
assert status == 'FINISHED'


####################### Agave file transfer##################################
#Transfer file from AGAVE_SOURCE_SYSTEM to AGAVE_DESTINATION_SYSTEM
FILE_TRANSFER= ag.files.importData(systemId=AGAVE_DESTINATION_SYSTEM,
                                  fileName=FILE_DEST,filePath='',
                                  urlToIngest=URL_TO_INGEST)
arsp = AgaveAsyncResponse(ag, FILE_TRANSFER)
status = arsp.result(timeout=200)
assert status == 'FINISHED'
print(status)
#print("remote path is " + REMOTE_PATH)
REMOTE_PATH=""  + FILE_DEST

#### History doesn't get populated instantly, we are waiting for 30s so History gets populated
#### The sleep time may vary depending on the file size

time.sleep(30)
#################### Transfer time computation using Agave Files History Endpoint ###################
# Check the history of file to get the times on statuses STAGGED and COMPLETED
# When you run this program for the second time it is important to delete the file on the destination system file, this will clear the history

HISTORY = ag.files.getHistory(filePath=REMOTE_PATH, systemId=AGAVE_DESTINATION_SYSTEM)
#print(HISTORY)
# Get the length of HISTORY
LAST_HISTORY_INDEX = len(HISTORY)-1

# Get Staging queued time ########
STAGING_QUEUED_TIME=HISTORY[0].created

# Get staging completed time#######
STAGING_COMPLETED_TIME=HISTORY[LAST_HISTORY_INDEX].created

# Take the time difference between the status completed and status QUEUED
DIFF=STAGING_COMPLETED_TIME - STAGING_QUEUED_TIME

print("Total time to transfer file (H:M:S): "+ str(DIFF) + " H:M:S")

# Get the local timestamp#########
localtime = time.asctime( time.localtime(time.time()) )

# Get detail time file spends in each status
time_queues=""
for i in range(1,len(HISTORY) ) :
       time_queues= time_queues + " " + str(i) +" "+  str(HISTORY[i].status) + " : " + str(HISTORY[i].created) +";"
print (time_queues)

# Write timing data to log file
with open(TRANSFER_TIME, "a") as myfile:
    myfile.write(" "+ str(localtime) + " time to transfer file (H:M:S):" + str(DIFF) + " "+time_queues+ "\n")


###### Files Clean up uncomment this block if needed #########
### Delete file on Source system
#FILE_DELETE=ag.files.delete(systemId=AGAVE_SOURCE_SYSTEM,
#                            filePath=FILE_SOURCE)

### Delete tranfered file on destination system
#FILE_DELETE=ag.files.delete(systemId=AGAVE_DESTINATION_SYSTEM,
#                         filePath=FILE_DEST)


######## End ########
