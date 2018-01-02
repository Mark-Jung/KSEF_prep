# -*- coding: utf-8 -*-

###############################################################################
#
# CopyReferenceSave
# Saves a copy reference returned by CopyReferenceGet to the user's Dropbox.
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

class CopyReferenceSave(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CopyReferenceSave Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CopyReferenceSave, self).__init__(temboo_session, '/Library/Dropbox/Files/CopyReferenceSave')


    def new_input_set(self):
        return CopyReferenceSaveInputSet()

    def _make_result_set(self, result, path):
        return CopyReferenceSaveResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CopyReferenceSaveChoreographyExecution(session, exec_id, path)

class CopyReferenceSaveInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CopyReferenceSave
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) The access token for a specific Dropbox user.)
        """
        super(CopyReferenceSaveInputSet, self)._set_input('AccessToken', value)
    def set_CopyReference(self, value):
        """
        Set the value of the CopyReference input for this Choreo. ((required, string) A copy reference returned by CopyReferenceGet.)
        """
        super(CopyReferenceSaveInputSet, self)._set_input('CopyReference', value)
    def set_Path(self, value):
        """
        Set the value of the Path input for this Choreo. ((required, string) Path in the user's Dropbox that is the destination.)
        """
        super(CopyReferenceSaveInputSet, self)._set_input('Path', value)

class CopyReferenceSaveResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CopyReferenceSave Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Dropbox.)
        """
        return self._output.get('Response', None)

class CopyReferenceSaveChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CopyReferenceSaveResultSet(response, path)
