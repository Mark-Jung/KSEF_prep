# -*- coding: utf-8 -*-

###############################################################################
#
# Predict
# Generates a prediction for the observation using the specified ML Model.
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

class Predict(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the Predict Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(Predict, self).__init__(temboo_session, '/Library/Amazon/MachineLearning/Predict')


    def new_input_set(self):
        return PredictInputSet()

    def _make_result_set(self, result, path):
        return PredictResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return PredictChoreographyExecution(session, exec_id, path)

class PredictInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the Predict
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AWSAccessKeyId(self, value):
        """
        Set the value of the AWSAccessKeyId input for this Choreo. ((required, string) The Access Key ID provided by Amazon Web Services.)
        """
        super(PredictInputSet, self)._set_input('AWSAccessKeyId', value)
    def set_AWSSecretKeyId(self, value):
        """
        Set the value of the AWSSecretKeyId input for this Choreo. ((required, string) The Secret Key ID provided by Amazon Web Services.)
        """
        super(PredictInputSet, self)._set_input('AWSSecretKeyId', value)
    def set_MLModelId(self, value):
        """
        Set the value of the MLModelId input for this Choreo. ((required, string) A unique identifier of the MLModel.)
        """
        super(PredictInputSet, self)._set_input('MLModelId', value)
    def set_PredictEndpoint(self, value):
        """
        Set the value of the PredictEndpoint input for this Choreo. ((required, string) The realtime endpoint to use for the prediction.)
        """
        super(PredictInputSet, self)._set_input('PredictEndpoint', value)
    def set_Record(self, value):
        """
        Set the value of the Record input for this Choreo. ((required, json) A map of variable name-value pairs that represent an observation.)
        """
        super(PredictInputSet, self)._set_input('Record', value)
    def set_UserRegion(self, value):
        """
        Set the value of the UserRegion input for this Choreo. ((optional, string) The AWS region that corresponds to the S3 endpoint you wish to access. The default region is "us-east-1".)
        """
        super(PredictInputSet, self)._set_input('UserRegion', value)

class PredictResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the Predict Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Amazon.)
        """
        return self._output.get('Response', None)

class PredictChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return PredictResultSet(response, path)
