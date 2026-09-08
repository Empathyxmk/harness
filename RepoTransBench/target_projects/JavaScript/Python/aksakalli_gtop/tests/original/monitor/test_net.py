import pytest
from unittest.mock import MagicMock

class Net:
    def __init__(self, spark):
        self.spark = spark

    def updateData(self, stats):
        self.spark.setData(stats)
        self.spark.screen.render()

def test_net_update_sets_data_and_renders():
    spark = MagicMock()
    spark.setData = MagicMock()
    spark.screen = MagicMock()
    spark.screen.render = MagicMock()
    net = Net(spark)
    net.updateData([{
        'iface': 'lo',
        'rx_sec': 12345,
        'tx_sec': 54321
    }])
    assert spark.setData.called
    assert spark.screen.render.called

def test_net_update_handles_no_data():
    spark = MagicMock()
    spark.setData = MagicMock()
    spark.screen = MagicMock()
    spark.screen.render = MagicMock()
    net = Net(spark)
    net.updateData([])
    assert spark.setData.called
    assert spark.screen.render.called