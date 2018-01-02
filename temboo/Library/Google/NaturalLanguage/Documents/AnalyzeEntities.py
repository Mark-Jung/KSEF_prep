# -*- coding: utf-8 -*-

###############################################################################
#
# AnalyzeEntities
# Finds named entities (currently proper names and common nouns) in the text along with entity types, salience, mentions for each entity, and other properties.
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

class AnalyzeEntities(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the AnalyzeEntities Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(AnalyzeEntities, self).__init__(temboo_session, '/Library/Google/NaturalLanguage/Documents/AnalyzeEntities')


    def new_input_set(self):
        return AnalyzeEntitiesInputSet()

    def _make_result_set(self, result, path):
        return AnalyzeEntitiesResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return AnalyzeEntitiesChoreographyExecution(session, exec_id, path)

class AnalyzeEntitiesInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the AnalyzeEntities
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_APIKey(self, value):
        """
        Set the value of the APIKey input for this Choreo. ((conditional, string) The API Key provided by Google.)
        """
        super(AnalyzeEntitiesInputSet, self)._set_input('APIKey', value)
    def set_Content(self, value):
        """
        Set the value of the Content input for this Choreo. ((conditional, string) The content to analyze.)
        """
        super(AnalyzeEntitiesInputSet, self)._set_input('Content', value)
    def set_EncodingType(self, value):
        """
        Set the value of the EncodingType input for this Choreo. ((optional, string) The encoding type used by the API to calculate sentence offsets. Defaults to UTF-8.)
        """
        super(AnalyzeEntitiesInputSet, self)._set_input('EncodingType', value)
    def set_Fields(self, value):
        """
        Set the value of the Fields input for this Choreo. ((optional, string) Selector specifying which fields to include in a partial response.)
        """
        super(AnalyzeEntitiesInputSet, self)._set_input('Fields', value)
    def set_GCSContentUri(self, value):
        """
        Set the value of the GCSContentUri input for this Choreo. ((optional, string) The Google Cloud Storage URI where the file content is located. This can be used instead of the Content input.)
        """
        super(AnalyzeEntitiesInputSet, self)._set_input('GCSContentUri', value)
    def set_Language(self, value):
        """
        Set the value of the Language input for this Choreo. ((optional, string) The language of the document. This is specified with the ISO-639-1 Code (e.g. "en"). If not specified, the language is detected if possible.)
        """
        super(AnalyzeEntitiesInputSet, self)._set_input('Language', value)
    def set_Type(self, value):
        """
        Set the value of the Type input for this Choreo. ((optional, string) The type of content being sent. Valid values are PLAIN_TEXT (the default) and HTML.)
        """
        super(AnalyzeEntitiesInputSet, self)._set_input('Type', value)

class AnalyzeEntitiesResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the AnalyzeEntities Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Google.)
        """
        return self._output.get('Response', None)

class AnalyzeEntitiesChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return AnalyzeEntitiesResultSet(response, path)
