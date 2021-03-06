#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from heat.engine.clients.os import senlin as senlin_plugin
from heat.tests import common
from heat.tests import utils
from senlinclient.common import exc


class SenlinClientPluginTest(common.HeatTestCase):

    def test_cluster_get(self):
        context = utils.dummy_context()
        plugin = context.clients.client_plugin('senlin')
        client = plugin.client()
        self.assertIsNotNone(client.clusters)

    def test_is_bad_request(self):
        context = utils.dummy_context()
        plugin = context.clients.client_plugin('senlin')
        self.assertTrue(plugin.is_bad_request(
            exc.sdkexc.HttpException(http_status=400)))
        self.assertFalse(plugin.is_bad_request(Exception))
        self.assertFalse(plugin.is_bad_request(
            exc.sdkexc.HttpException(http_status=404)))


class ProfileConstraintTest(common.HeatTestCase):

    def setUp(self):
        super(ProfileConstraintTest, self).setUp()
        self.senlin_client = mock.MagicMock()
        self.ctx = utils.dummy_context()
        self.mock_get_profile = mock.Mock()
        self.ctx.clients.client(
            'senlin').get_profile = self.mock_get_profile
        self.constraint = senlin_plugin.ProfileConstraint()

    def test_validate_true(self):
        self.mock_get_profile.return_value = None
        self.assertTrue(self.constraint.validate("PROFILE_ID", self.ctx))

    def test_validate_false(self):
        self.mock_get_profile.side_effect = exc.sdkexc.ResourceNotFound(
            'PROFILE_ID')
        self.assertFalse(self.constraint.validate("PROFILE_ID", self.ctx))
        self.mock_get_profile.side_effect = exc.sdkexc.HttpException(
            'PROFILE_ID')
        self.assertFalse(self.constraint.validate("PROFILE_ID", self.ctx))


class ClusterConstraintTest(common.HeatTestCase):

    def setUp(self):
        super(ClusterConstraintTest, self).setUp()
        self.senlin_client = mock.MagicMock()
        self.ctx = utils.dummy_context()
        self.mock_get_cluster = mock.Mock()
        self.ctx.clients.client(
            'senlin').get_cluster = self.mock_get_cluster
        self.constraint = senlin_plugin.ClusterConstraint()

    def test_validate_true(self):
        self.mock_get_cluster.return_value = None
        self.assertTrue(self.constraint.validate("CLUSTER_ID", self.ctx))

    def test_validate_false(self):
        self.mock_get_cluster.side_effect = exc.sdkexc.ResourceNotFound(
            'CLUSTER_ID')
        self.assertFalse(self.constraint.validate("CLUSTER_ID", self.ctx))
        self.mock_get_cluster.side_effect = exc.sdkexc.HttpException(
            'CLUSTER_ID')
        self.assertFalse(self.constraint.validate("CLUSTER_ID", self.ctx))


class ProfileTypeConstraintTest(common.HeatTestCase):

    def setUp(self):
        super(ProfileTypeConstraintTest, self).setUp()
        self.senlin_client = mock.MagicMock()
        self.ctx = utils.dummy_context()
        self.mock_profile_types = mock.Mock(
            return_value=[{'name': 'os.heat.stack-1.0'},
                          {'name': 'os.nova.server-1.0'}])
        self.ctx.clients.client(
            'senlin').profile_types = self.mock_profile_types
        self.constraint = senlin_plugin.ProfileTypeConstraint()

    def test_validate_true(self):
        self.assertTrue(self.constraint.validate("os.heat.stack-1.0",
                                                 self.ctx))

    def test_validate_false(self):
        self.assertFalse(self.constraint.validate("Invalid_type",
                                                  self.ctx))


class PolicyTypeConstraintTest(common.HeatTestCase):

    def setUp(self):
        super(PolicyTypeConstraintTest, self).setUp()
        self.senlin_client = mock.MagicMock()
        self.ctx = utils.dummy_context()
        self.mock_policy_types = mock.Mock(
            return_value=[{'name': 'senlin.policy.deletion-1.0'},
                          {'name': 'senlin.policy.loadbalance-1.0'}])
        self.ctx.clients.client(
            'senlin').policy_types = self.mock_policy_types
        self.constraint = senlin_plugin.PolicyTypeConstraint()

    def test_validate_true(self):
        self.assertTrue(self.constraint.validate(
            "senlin.policy.deletion-1.0", self.ctx))

    def test_validate_false(self):
        self.assertFalse(self.constraint.validate("Invalid_type",
                                                  self.ctx))
