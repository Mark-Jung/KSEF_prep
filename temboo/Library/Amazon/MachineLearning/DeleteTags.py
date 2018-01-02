# -*- coding: utf-8 -*-

###############################################################################
#
# DeleteTags
# Deletes the specified tags associated with an ML object.
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

class DeleteTags(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the DeleteTags Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(DeleteTags, self).__init__(temboo_session, '/Library/Amazon/MachineLearning/DeleteTags')


    def new_input_set(self):
        return DeleteTagsInputSet()

    def _make_result_set(self, result, path):
        return DeleteTagsResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return DeleteTagsChoreographyExecution(session, exec_id, path)

class DeleteTagsInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the DeleteTags
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AWSAccessKeyId(self, value):
        """
        Set the value of the AWSAccessKeyId input for this Choreo. ((required, string) The Access Key ID provided by Amazon Web Services.)
        """
        super(DeleteTagsInputSet, self)._set_input('AWSAccessKeyId', value)
    def set_AWSSecretKeyId(self, value):
        """
        Set the value of the AWSSecretKeyId input for this Choreo. ((required, string) The Secret Key ID provided by Amazon Web Services.)
        """
        super(DeleteTagsInputSet, self)._set_input('AWSSecretKeyId', value)
    def set_ResourceId(self, value):
        """
        Set the value of the ResourceId input for this Choreo. ((required, string) The ID of the ML object to tag.)
        """
        super(DeleteTagsInputSet, self)._set_input('ResourceId', value)
    def set_ResourceType(self, value):
        """
        Set the value of the ResourceType input for this Choreo. ((required, string) The type of the ML object to tag. Valid values are: BatchPrediction, DataSource, Evaluation, MLModel.)
        """
        super(DeleteTagsInputSet, self)._set_input('ResourceType', value)
    def set_TagKeys(self, value):
        """
        Set the value of the TagKeys input for this Choreo. ((required, json) One or more tags to delete.)
        """
        super(DeleteTagsInputSet, self)._set_input('TagKeys', value)
    def set_UserRegion(self, value):
        """
        Set the value of the UserRegion input for this Choreo. ((optional, string) The AWS region that corresponds to the S3 endpoint you wish to access. The default region is "us-east-1".)
        """
        super(DeleteTagsInputSet, self)._set_input('UserRegion', value)

class DeleteTagsResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the DeleteTags Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Amazon.)
        """
        return self._output.get('Response', None)

class DeleteTagsChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return DeleteTagsResultSet(response, path)
