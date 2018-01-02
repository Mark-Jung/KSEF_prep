# -*- coding: utf-8 -*-

###############################################################################
#
# CreateBatchPrediction
# Generates predictions for a group of observations.
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

class CreateBatchPrediction(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CreateBatchPrediction Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CreateBatchPrediction, self).__init__(temboo_session, '/Library/Amazon/MachineLearning/CreateBatchPrediction')


    def new_input_set(self):
        return CreateBatchPredictionInputSet()

    def _make_result_set(self, result, path):
        return CreateBatchPredictionResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CreateBatchPredictionChoreographyExecution(session, exec_id, path)

class CreateBatchPredictionInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CreateBatchPrediction
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AWSAccessKeyId(self, value):
        """
        Set the value of the AWSAccessKeyId input for this Choreo. ((required, string) The Access Key ID provided by Amazon Web Services.)
        """
        super(CreateBatchPredictionInputSet, self)._set_input('AWSAccessKeyId', value)
    def set_AWSSecretKeyId(self, value):
        """
        Set the value of the AWSSecretKeyId input for this Choreo. ((required, string) The Secret Key ID provided by Amazon Web Services.)
        """
        super(CreateBatchPredictionInputSet, self)._set_input('AWSSecretKeyId', value)
    def set_BatchPredictionDataSourceId(self, value):
        """
        Set the value of the BatchPredictionDataSourceId input for this Choreo. ((required, string) The ID of the DataSource that points to the group of observations to predict.)
        """
        super(CreateBatchPredictionInputSet, self)._set_input('BatchPredictionDataSourceId', value)
    def set_BatchPredictionId(self, value):
        """
        Set the value of the BatchPredictionId input for this Choreo. ((required, string) A user-supplied ID that uniquely identifies the BatchPrediction.)
        """
        super(CreateBatchPredictionInputSet, self)._set_input('BatchPredictionId', value)
    def set_BatchPredictionName(self, value):
        """
        Set the value of the BatchPredictionName input for this Choreo. ((optional, string) A user-supplied name or description of the BatchPrediction.)
        """
        super(CreateBatchPredictionInputSet, self)._set_input('BatchPredictionName', value)
    def set_MLModelId(self, value):
        """
        Set the value of the MLModelId input for this Choreo. ((required, string) The ID of the MLModel that will generate predictions for the group of observations.)
        """
        super(CreateBatchPredictionInputSet, self)._set_input('MLModelId', value)
    def set_OutputUri(self, value):
        """
        Set the value of the OutputUri input for this Choreo. ((required, string) The location of an Amazon S3 bucket or directory to store the batch prediction results.)
        """
        super(CreateBatchPredictionInputSet, self)._set_input('OutputUri', value)
    def set_UserRegion(self, value):
        """
        Set the value of the UserRegion input for this Choreo. ((optional, string) The AWS region that corresponds to the S3 endpoint you wish to access. The default region is "us-east-1".)
        """
        super(CreateBatchPredictionInputSet, self)._set_input('UserRegion', value)

class CreateBatchPredictionResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CreateBatchPrediction Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Amazon.)
        """
        return self._output.get('Response', None)

class CreateBatchPredictionChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CreateBatchPredictionResultSet(response, path)
