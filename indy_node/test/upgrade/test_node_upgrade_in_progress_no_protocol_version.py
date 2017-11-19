import pytest

from indy_common.constants import IN_PROGRESS
from indy_node.test.helper import TestNode
from indy_node.test.upgrade.helper import check_node_sent_acknowledges_upgrade

whitelist = ['unable to send message']


class TestNodeNoProtocolVersion(TestNode):
    def processNodeRequest(self, request, frm):
        if request.protocolVersion is not None:
            raise ValueError('Do not understand what protocolVersion is!!!')
        super().processNodeRequest(request, frm)


@pytest.fixture(scope="module")
def testNodeClass(patchPluginManager):
    return TestNodeNoProtocolVersion


def test_node_sent_upgrade_in_progress_no_protocol_version(looper, nodeSet, nodeIds, validUpgrade):
    '''
    Test that each node sends NODE_UPGRADE In Progress event
    (because it sees scheduledUpgrade in the Upgrader)
    '''
    version = validUpgrade['version']
    for node, node_id in zip(nodeSet, nodeIds):
        node.upgrader.scheduledUpgrade = (version,
                                          validUpgrade['schedule'][node_id],
                                          "upgrade_id")
        node.notify_upgrade_start()
    check_node_sent_acknowledges_upgrade(looper, nodeSet, nodeIds,
                                         allowed_actions=[IN_PROGRESS],
                                         ledger_size=len(nodeSet),
                                         expected_version=version)
