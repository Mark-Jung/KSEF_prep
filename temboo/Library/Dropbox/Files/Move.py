# -*- coding: utf-8 -*-

###############################################################################
#
# Move
# Moves a file or folder to a different location in the user's Dropbox.
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

class Move(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the Move Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(Move, self).__init__(temboo_session, '/Library/Dropbox/Files/Move')


    def new_input_set(self):
        return MoveInputSet()

    def _make_result_set(self, result, path):
        return MoveResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return MoveChoreographyExecution(session, exec_id, path)

class MoveInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the Move
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) The access token for a specific Dropbox user.)
        """
        super(MoveInputSet, self)._set_input('AccessToken', value)
    def set_AllowSharedFolder(self, value):
        """
        Set the value of the AllowSharedFolder input for this Choreo. ((optional, boolean) If true, contents are copied into a shared folder, otherwise an error will be returned if the FromPath contains a shared folder. The default for this field is false.)
        """
        super(MoveInputSet, self)._set_input('AllowSharedFolder', value)
    def set_AutoRename(self, value):
        """
        Set the value of the AutoRename input for this Choreo. ((optional, boolean) If there's a conflict, have the Dropbox server try to autorename the file to avoid the conflict. The default for this field is false.)
        """
        super(MoveInputSet, self)._set_input('AutoRename', value)
    def set_FromPath(self, value):
        """
        Set the value of the FromPath input for this Choreo. ((required, string) Path in the user's Dropbox to be copied or moved.)
        """
        super(MoveInputSet, self)._set_input('FromPath', value)
    def set_ToPath(self, value):
        """
        Set the value of the ToPath input for this Choreo. ((required, string) Path in the user's Dropbox that is the destination.)
        """
        super(MoveInputSet, self)._set_input('ToPath', value)

class MoveResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the Move Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Dropbox.)
        """
        return self._output.get('Response', None)

class MoveChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return MoveResultSet(response, path)
