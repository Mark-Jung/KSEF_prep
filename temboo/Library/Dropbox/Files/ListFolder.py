# -*- coding: utf-8 -*-

###############################################################################
#
# ListFolder
# Starts returning the contents of a folder.
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

class ListFolder(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the ListFolder Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(ListFolder, self).__init__(temboo_session, '/Library/Dropbox/Files/ListFolder')


    def new_input_set(self):
        return ListFolderInputSet()

    def _make_result_set(self, result, path):
        return ListFolderResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return ListFolderChoreographyExecution(session, exec_id, path)

class ListFolderInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the ListFolder
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) The access token for a specific Dropbox user.)
        """
        super(ListFolderInputSet, self)._set_input('AccessToken', value)
    def set_IncludeDeleted(self, value):
        """
        Set the value of the IncludeDeleted input for this Choreo. ((optional, boolean) If true, the results will include entries for files and folders that used to exist but were deleted. The default for this field is false.)
        """
        super(ListFolderInputSet, self)._set_input('IncludeDeleted', value)
    def set_IncludeHasExplicitSharedMembers(self, value):
        """
        Set the value of the IncludeHasExplicitSharedMembers input for this Choreo. ((optional, boolean) If true, the results will include a flag for each file indicating whether or not that file has any explicit members. The default for this field is false.)
        """
        super(ListFolderInputSet, self)._set_input('IncludeHasExplicitSharedMembers', value)
    def set_IncludeMediaInfo(self, value):
        """
        Set the value of the IncludeMediaInfo input for this Choreo. ((optional, boolean) If true, FileMetadata.media_info is set for photo and video. The default for this field is false.)
        """
        super(ListFolderInputSet, self)._set_input('IncludeMediaInfo', value)
    def set_Path(self, value):
        """
        Set the value of the Path input for this Choreo. ((required, string) The path to the folder you want to see the contents of. This should be empty to list contents at the root level.)
        """
        super(ListFolderInputSet, self)._set_input('Path', value)
    def set_Recursive(self, value):
        """
        Set the value of the Recursive input for this Choreo. ((optional, boolean) If true, the list folder operation will be applied recursively to all subfolders and the response will contain contents of all subfolders. The default for this field is false.)
        """
        super(ListFolderInputSet, self)._set_input('Recursive', value)

class ListFolderResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the ListFolder Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Cursor(self):
        """
        Retrieve the value for the "Cursor" output from this Choreo execution. ((string) A cursor used to retrieve the next set of results with ListFolderContinue.)
        """
        return self._output.get('Cursor', None)
    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Dropbox.)
        """
        return self._output.get('Response', None)

class ListFolderChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return ListFolderResultSet(response, path)
