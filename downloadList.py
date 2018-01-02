# -*- coding: utf-8 -*-
from temboo.Library.Dropbox.Files import Download
from temboo.core.session import TembooSession

def getList():
    # Create a session with your Temboo account details
    session = TembooSession("bb20170815", "myFirstApp", "WMENs2Yj3qmoY8ydMLYulDnWn67IoZFS") #매달 바뀌는 듯
    
    # Instantiate the Choreo
    downloadChoreo = Download(session)
    
    # Get an InputSet object for the Choreo
    downloadInputs = downloadChoreo.new_input_set()
    
    # Set the Choreo inputs
    downloadInputs.set_Path("suspectList.txt")
    downloadInputs.set_AccessToken("1rshKArZ-mAAAAAAAAAAC-FE7-1OOeVCK5XqR5LbcShXzWN9TLDpIVgSU0sjbCKL")
    downloadInputs.set_Encode("false")
    
    # Execute the Choreo
    downloadResults = downloadChoreo.execute_with_results(downloadInputs)
    
    strA = downloadResults.get_Response()
    
    return strA
