# -*- coding: utf-8 -*-

###############################################################################
#
# FromOAuth1
# Creates an OAuth 2.0 access token from the supplied OAuth 1.0 access token.
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

class FromOAuth1(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the FromOAuth1 Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(FromOAuth1, self).__init__(temboo_session, '/Library/Dropbox/OAuth/FromOAuth1')


    def new_input_set(self):
        return FromOAuth1InputSet()

    def _make_result_set(self, result, path):
        return FromOAuth1ResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return FromOAuth1ChoreographyExecution(session, exec_id, path)

class FromOAuth1InputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the FromOAuth1
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((required, string) An OAuth 1.0 access token for a specific Dropbox user.)
        """
        super(FromOAuth1InputSet, self)._set_input('AccessToken', value)
    def set_AccessTokenSecret(self, value):
        """
        Set the value of the AccessTokenSecret input for this Choreo. ((required, string) An OAuth 1.0 access token secret for a specific Dropbox user.)
        """
        super(FromOAuth1InputSet, self)._set_input('AccessTokenSecret', value)
    def set_AppKey(self, value):
        """
        Set the value of the AppKey input for this Choreo. ((required, string) The App Key provided by Dropbox after registering your application.)
        """
        super(FromOAuth1InputSet, self)._set_input('AppKey', value)
    def set_AppSecret(self, value):
        """
        Set the value of the AppSecret input for this Choreo. ((required, string) The App Secret provided by Dropbox after registering your application.)
        """
        super(FromOAuth1InputSet, self)._set_input('AppSecret', value)

class FromOAuth1ResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the FromOAuth1 Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_OAuth2AccessToken(self):
        """
        Retrieve the value for the "OAuth2AccessToken" output from this Choreo execution. ((string) The OAuth 2.0 access for a specific Dropbox user.)
        """
        return self._output.get('OAuth2AccessToken', None)

class FromOAuth1ChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return FromOAuth1ResultSet(response, path)
