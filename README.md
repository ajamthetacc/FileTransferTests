# FileTransferTests
Agave file transfer tests cdc
Filetransfer.py is used to transfer files between two hosts(storage systems) and compute, the transfer time using Agave Files API calls
 File transfer is done between two Agave storage systems, which have different underlying hosts but are registered with same tenant
 This script requires following command line arguments
 arg 1 : Base url for the tenant
 arg 2:  Authorization token
 arg 3:  Absolute path of the file to store response time log
 arg 4:  Agave storage system name from where file transfer will initiate (source), we call it AGAVE_SOURCE_SYSTEM
 arg 5:  Agave storage system where file will be transfered (destination), we call it AGAVE_DESTINATION_SYSTEM
 Run as : run Filetransfer.py $Base_url $Token $LofFilePath $AgaveSourceSystemName $AgaveDestinationSystemName
 You will need to install Agave py. Installation details can be found at https://github.com/TACC/agavepy/blob/master/README.rst
