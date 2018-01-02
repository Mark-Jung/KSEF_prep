# -*- coding: utf-8 -*-

###############################################################################
#
# CreateMLModel
# Creates a new MLModel using the DataSource and the recipe as information sources.
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

class CreateMLModel(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CreateMLModel Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CreateMLModel, self).__init__(temboo_session, '/Library/Amazon/MachineLearning/CreateMLModel')


    def new_input_set(self):
        return CreateMLModelInputSet()

    def _make_result_set(self, result, path):
        return CreateMLModelResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CreateMLModelChoreographyExecution(session, exec_id, path)

class CreateMLModelInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CreateMLModel
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AWSAccessKeyId(self, value):
        """
        Set the value of the AWSAccessKeyId input for this Choreo. ((required, string) The Access Key ID provided by Amazon Web Services.)
        """
        super(CreateMLModelInputSet, self)._set_input('AWSAccessKeyId', value)
    def set_AWSSecretKeyId(self, value):
        """
        Set the value of the AWSSecretKeyId input for this Choreo. ((required, string) The Secret Key ID provided by Amazon Web Services.)
        """
        super(CreateMLModelInputSet, self)._set_input('AWSSecretKeyId', value)
    def set_MLModelId(self, value):
        """
        Set the value of the MLModelId input for this Choreo. ((required, string) A user-supplied identifier that uniquely identifies the MLModel.)
        """
        super(CreateMLModelInputSet, self)._set_input('MLModelId', value)
    def set_MLModelName(self, value):
        """
        Set the value of the MLModelName input for this Choreo. ((optional, string) A user-supplied name or description of the MLModel.)
        """
        super(CreateMLModelInputSet, self)._set_input('MLModelName', value)
    def set_MLModelType(self, value):
        """
        Set the value of the MLModelType input for this Choreo. ((required, string) The category of supervised learning that this MLModel will address. Choose from the following types: REGRESSION, BINARY, MULTICLASS.)
        """
        super(CreateMLModelInputSet, self)._set_input('MLModelType', value)
    def set_Parameters(self, value):
        """
        Set the value of the Parameters input for this Choreo. ((optional, json) A list of the training parameters in the MLModel. The list is implemented as a map of key-value pairs.)
        """
        super(CreateMLModelInputSet, self)._set_input('Parameters', value)
    def set_Recipe(self, value):
        """
        Set the value of the Recipe input for this Choreo. ((optional, string) The data recipe for creating the MLModel. You must specify either the recipe or its URI. If you don't specify a recipe or its URI, Amazon ML creates a default.)
        """
        super(CreateMLModelInputSet, self)._set_input('Recipe', value)
    def set_RecipeUri(self, value):
        """
        Set the value of the RecipeUri input for this Choreo. ((optional, string) The Amazon S3 location and file name that contains the MLModel recipe. You must specify either the recipe or its URI. If you don't specify a recipe or its URI, Amazon ML creates a default.)
        """
        super(CreateMLModelInputSet, self)._set_input('RecipeUri', value)
    def set_TrainingDataSourceId(self, value):
        """
        Set the value of the TrainingDataSourceId input for this Choreo. ((required, string) The DataSource that points to the training data.)
        """
        super(CreateMLModelInputSet, self)._set_input('TrainingDataSourceId', value)
    def set_UserRegion(self, value):
        """
        Set the value of the UserRegion input for this Choreo. ((optional, string) The AWS region that corresponds to the S3 endpoint you wish to access. The default region is "us-east-1".)
        """
        super(CreateMLModelInputSet, self)._set_input('UserRegion', value)

class CreateMLModelResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CreateMLModel Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Amazon.)
        """
        return self._output.get('Response', None)

class CreateMLModelChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CreateMLModelResultSet(response, path)
