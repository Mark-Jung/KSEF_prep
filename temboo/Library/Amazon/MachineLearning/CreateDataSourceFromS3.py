# -*- coding: utf-8 -*-

###############################################################################
#
# CreateDataSourceFromS3
# Creates a DataSource object.
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

class CreateDataSourceFromS3(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CreateDataSourceFromS3 Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CreateDataSourceFromS3, self).__init__(temboo_session, '/Library/Amazon/MachineLearning/CreateDataSourceFromS3')


    def new_input_set(self):
        return CreateDataSourceFromS3InputSet()

    def _make_result_set(self, result, path):
        return CreateDataSourceFromS3ResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CreateDataSourceFromS3ChoreographyExecution(session, exec_id, path)

class CreateDataSourceFromS3InputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CreateDataSourceFromS3
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AWSAccessKeyId(self, value):
        """
        Set the value of the AWSAccessKeyId input for this Choreo. ((required, string) The Access Key ID provided by Amazon Web Services.)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('AWSAccessKeyId', value)
    def set_AWSSecretKeyId(self, value):
        """
        Set the value of the AWSSecretKeyId input for this Choreo. ((required, string) The Secret Key ID provided by Amazon Web Services.)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('AWSSecretKeyId', value)
    def set_ComputeStatistics(self, value):
        """
        Set the value of the ComputeStatistics input for this Choreo. ((optional, boolean) The compute statistics for a DataSource. This parameter must be set to true if the DataSource needs to be used for MLModel training. Defaults to false.)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('ComputeStatistics', value)
    def set_DataLocationS3(self, value):
        """
        Set the value of the DataLocationS3 input for this Choreo. ((required, string) The location of the data file(s) used by a DataSource. The URI specifies a data file or an Amazon Simple Storage Service (Amazon S3) directory or bucket containing data files.)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('DataLocationS3', value)
    def set_DataRearrangement(self, value):
        """
        Set the value of the DataRearrangement input for this Choreo. ((optional, json) A JSON string that represents the splitting and rearrangement requirements for the Datasource.)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('DataRearrangement', value)
    def set_DataSchema(self, value):
        """
        Set the value of the DataSchema input for this Choreo. ((optional, json) A JSON string representing the schema. This is required unless specifying a valid URI for DataSchemaLocationS3.)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('DataSchema', value)
    def set_DataSchemaLocationS3(self, value):
        """
        Set the value of the DataSchemaLocationS3 input for this Choreo. ((conditional, string) The Amazon S3 location of the DataSchema. This is required unless specifying a valid JSON schema file for DataSchema (see optional inputs).)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('DataSchemaLocationS3', value)
    def set_DataSourceId(self, value):
        """
        Set the value of the DataSourceId input for this Choreo. ((required, string) A user-supplied identifier that uniquely identifies the DataSource.)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('DataSourceId', value)
    def set_DataSourceName(self, value):
        """
        Set the value of the DataSourceName input for this Choreo. ((optional, string) A user-supplied name or description of the DataSource.)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('DataSourceName', value)
    def set_UserRegion(self, value):
        """
        Set the value of the UserRegion input for this Choreo. ((optional, string) The AWS region that corresponds to the S3 endpoint you wish to access. The default region is "us-east-1".)
        """
        super(CreateDataSourceFromS3InputSet, self)._set_input('UserRegion', value)

class CreateDataSourceFromS3ResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CreateDataSourceFromS3 Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from Amazon.)
        """
        return self._output.get('Response', None)

class CreateDataSourceFromS3ChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CreateDataSourceFromS3ResultSet(response, path)
