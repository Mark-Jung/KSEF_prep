# -*- coding: utf-8 -*-

###############################################################################
#
# CreateFolder
# Creates a folder at a given path.
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

class CreateFolder(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CreateFolder Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CreateFolder, self).__init__(temboo_session, '/Library/Dropbox/Files/CreateFolder')


    def new_input_set(self):
        return CreateFolderInputSet()

    def _make_result_set(self, result, path):
        return CreateFolderResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CreateFolderChoreographyExecution(session, exec_id, path)

class CreateFolderInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CreateFolder
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) The access token for a specific Dropbox user.)
        """
        super(CreateFolderInputSet, self)._set_input('AccessToken', value)
    def set_AutoRename(self, value):
        """
        Set the value of the AutoRename input for this Choreo. ((optional, boolean) If there's a conflict, have the Dropbox server try to autorename the file to avoid the conflict. The default for this field is false.)
        """
        super(CreateFolderInputSet, self)._set_input('AutoRename', value)
    def set_Path(self, value):
        """
        Set the value of the Path input for this Choreo. ((required, string) Path in the user's Dropbox to create.)
        """
        super(CreateFolderInputSet, self)._set_input('Path', value)

class CreateFolderResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CreateFolder Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Dropbox.)
        """
        return self._output.get('Response', None)

class CreateFolderChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CreateFolderResultSet(response, path)
