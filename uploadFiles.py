# -*- coding: utf-8 -*-
from temboo.Library.Dropbox.Files import Upload
from temboo.core.session import TembooSession
import base64

def upload(strData):  #번호4자리
    # Create a session with your Temboo account details
    session = TembooSession("bb20170815", "myFirstApp", "WMENs2Yj3qmoY8ydMLYulDnWn67IoZFS") #매달 바뀌는 듯
    
    # Instantiate the Choreo
    uploadChoreo = Upload(session)
    
    # Get an InputSet object for the Choreo
    uploadInputs = uploadChoreo.new_input_set()
    uploadInputs.set_AccessToken("1rshKArZ-mAAAAAAAAAAC-FE7-1OOeVCK5XqR5LbcShXzWN9TLDpIVgSU0sjbCKL")
        
    fileNames=[]
    imgFileName = strData + ".IMG.jpg"
    locFileName = strData + ".LOC.html"
    fileNames.append(imgFileName)
    fileNames.append(locFileName)

    for fileName in fileNames:
        # Encode file
        with open(fileName, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        
        # Set the Choreo inputs
        serverPath = "/suspect/" + fileName
        uploadInputs.set_Path(serverPath)
        uploadInputs.set_FileContent(encoded_string)
        
        # Execute the Choreo
        uploadResults = uploadChoreo.execute_with_results(uploadInputs)
        
        # Print the Choreo outputs
        print("Response: " + uploadResults.get_Response())
    
 
