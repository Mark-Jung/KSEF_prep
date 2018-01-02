# -*- coding: utf-8 -*-

###############################################################################
#
# Upload
# Creates a new file with the contents provided in the request.
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

class Upload(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the Upload Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(Upload, self).__init__(temboo_session, '/Library/Dropbox/Files/Upload')


    def new_input_set(self):
        return UploadInputSet()

    def _make_result_set(self, result, path):
        return UploadResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return UploadChoreographyExecution(session, exec_id, path)

class UploadInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the Upload
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) The access token for a specific Dropbox user.)
        """
        super(UploadInputSet, self)._set_input('AccessToken', value)
    def set_AutoRename(self, value):
        """
        Set the value of the AutoRename input for this Choreo. ((optional, boolean) If there's a conflict, as determined by mode, have the Dropbox server try to autorename the file to avoid conflict. The default for this field is false.)
        """
        super(UploadInputSet, self)._set_input('AutoRename', value)
    def set_ContentType(self, value):
        """
        Set the value of the ContentType input for this Choreo. ((optional, string) The content type of the file being uploaded. Defaults to application/octet-stream.)
        """
        super(UploadInputSet, self)._set_input('ContentType', value)
    def set_FileContent(self, value):
        """
        Set the value of the FileContent input for this Choreo. ((conditional, string) The Base64-encoded file content of the file you want to upload. Required unless uploading a file from a URL using the FileURL input. Encoding is not required when ContentType is set to "text/plain".)
        """
        super(UploadInputSet, self)._set_input('FileContent', value)
    def set_FileURL(self, value):
        """
        Set the value of the FileURL input for this Choreo. ((optional, string) The public URL for file you want to upload. This can be used as an alternative to uploading Base64 encoded data.)
        """
        super(UploadInputSet, self)._set_input('FileURL', value)
    def set_Mode(self, value):
        """
        Set the value of the Mode input for this Choreo. ((optional, string) Selects what to do if the file already exists. Valid values are: add (default), overwrite, and update.)
        """
        super(UploadInputSet, self)._set_input('Mode', value)
    def set_Mute(self, value):
        """
        Set the value of the Mute input for this Choreo. ((optional, boolean) If true, this tells the clients that this modification shouldn't result in a user notification. The default for this field is false.)
        """
        super(UploadInputSet, self)._set_input('Mute', value)
    def set_Path(self, value):
        """
        Set the value of the Path input for this Choreo. ((required, string) Path in the user's Dropbox to save the file, including the filename.)
        """
        super(UploadInputSet, self)._set_input('Path', value)
    def set_Revision(self, value):
        """
        Set the value of the Revision input for this Choreo. ((optional, string) The revision identifier. Used only when Mode is set to "update".)
        """
        super(UploadInputSet, self)._set_input('Revision', value)

class UploadResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the Upload Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Dropbox.)
        """
        return self._output.get('Response', None)

class UploadChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return UploadResultSet(response, path)
