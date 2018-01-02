# -*- coding: utf-8 -*-

###############################################################################
#
# ListFolderContinue
# Once a cursor has been retrieved from ListFolder, use this to paginate through all files and retrieve updates to the folder.
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

class ListFolderContinue(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the ListFolderContinue Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(ListFolderContinue, self).__init__(temboo_session, '/Library/Dropbox/Files/ListFolderContinue')


    def new_input_set(self):
        return ListFolderContinueInputSet()

    def _make_result_set(self, result, path):
        return ListFolderContinueResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return ListFolderContinueChoreographyExecution(session, exec_id, path)

class ListFolderContinueInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the ListFolderContinue
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) The access token for a specific Dropbox user.)
        """
        super(ListFolderContinueInputSet, self)._set_input('AccessToken', value)
    def set_Cursor(self, value):
        """
        Set the value of the Cursor input for this Choreo. ((required, string) A cursor used to retrieve the next set of results.)
        """
        super(ListFolderContinueInputSet, self)._set_input('Cursor', value)

class ListFolderContinueResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the ListFolderContinue Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_LatestCursor(self):
        """
        Retrieve the value for the "LatestCursor" output from this Choreo execution. ((string) The latest cursor which can be used to retrieve the next set of results.)
        """
        return self._output.get('LatestCursor', None)
    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Dropbox.)
        """
        return self._output.get('Response', None)

class ListFolderContinueChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return ListFolderContinueResultSet(response, path)
