# -*- coding: utf-8 -*-

###############################################################################
#
# CreateSharedLink
# Creates a shared link.
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

class CreateSharedLink(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CreateSharedLink Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CreateSharedLink, self).__init__(temboo_session, '/Library/Dropbox/Sharing/CreateSharedLink')


    def new_input_set(self):
        return CreateSharedLinkInputSet()

    def _make_result_set(self, result, path):
        return CreateSharedLinkResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CreateSharedLinkChoreographyExecution(session, exec_id, path)

class CreateSharedLinkInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CreateSharedLink
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) The access token for a specific Dropbox user.)
        """
        super(CreateSharedLinkInputSet, self)._set_input('AccessToken', value)
    def set_Path(self, value):
        """
        Set the value of the Path input for this Choreo. ((required, string) The path to share.)
        """
        super(CreateSharedLinkInputSet, self)._set_input('Path', value)
    def set_ShortURL(self, value):
        """
        Set the value of the ShortURL input for this Choreo. ((optional, boolean) Whether to return a shortened URL. The default for this field is false.)
        """
        super(CreateSharedLinkInputSet, self)._set_input('ShortURL', value)

class CreateSharedLinkResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CreateSharedLink Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Dropbox.)
        """
        return self._output.get('Response', None)

class CreateSharedLinkChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CreateSharedLinkResultSet(response, path)
