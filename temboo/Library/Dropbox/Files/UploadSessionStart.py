# -*- coding: utf-8 -*-

###############################################################################
#
# UploadSessionStart
# Allows you to upload a single file in one or more requests. This call starts a new upload session with the first chunk of data.
#
# Python versions 2.6, 2.7, 3.x
#
# Copyright 2014, Temboo Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
#
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class UploadSessionStart(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the UploadSessionStart Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(UploadSessionStart, self).__init__(temboo_session, '/Library/Dropbox/Files/UploadSessionStart')


    def new_input_set(self):
        return UploadSessionStartInputSet()

    def _make_result_set(self, result, path):
        return UploadSessionStartResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return UploadSessionStartChoreographyExecution(session, exec_id, path)

class UploadSessionStartInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the UploadSessionStart
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) The access token for a specific Dropbox user.)
        """
        super(UploadSessionStartInputSet, self)._set_input('AccessToken', value)
    def set_Close(self, value):
        """
        Set the value of the Close input for this Choreo. ((optional, boolean) If true, the current session will be closed, at which point you won't be able to call UploadSessionAppend anymore with the current session. The default for this field is false.)
        """
        super(UploadSessionStartInputSet, self)._set_input('Close', value)
    def set_ContentType(self, value):
        """
        Set the value of the ContentType input for this Choreo. ((optional, string) The content type of the file being uploaded. Defaults to application/octet-stream.)
        """
        super(UploadSessionStartInputSet, self)._set_input('ContentType', value)
    def set_FileContent(self, value):
        """
        Set the value of the FileContent input for this Choreo. ((conditional, string) The first file segment to upload. Binary files should be Base64-encoded. Encoding is not required when ContentType is set to "text/plain".)
        """
        super(UploadSessionStartInputSet, self)._set_input('FileContent', value)

class UploadSessionStartResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the UploadSessionStart Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_SessionID(self):
        """
        Retrieve the value for the "SessionID" output from this Choreo execution. ((string) The upload session ID that can be used to append to the upload or finish the upload.)
        """
        return self._output.get('SessionID', None)

class UploadSessionStartChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return UploadSessionStartResultSet(response, path)
