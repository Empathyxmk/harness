import sys
import os
import pathlib

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import graphios

def test_public_create_metric_line():
    # Use different data than the default tests
    if hasattr(graphios, "create_metric_line"):
        line = graphios.create_metric_line('disk_usage', 'server3', 'DiskIO', 'write', 0.99, 456, 678, '2024-02-10 08:00:00')
        assert line == 'disk_usage,server3,DiskIO,write,0.99,456,678,2024-02-10 08:00:00'

def test_public_parse_value():
    if hasattr(graphios, "parse_value"):
        assert graphios.parse_value('52.34') == 52.34
        assert graphios.parse_value('off') == 'off'

def test_public_format_perfdata():
    if hasattr(graphios, "format_perfdata"):
        pd = {'label': 'free_mem', 'value': 1234, 'uom': 'MB', 'warn': '', 'crit': '', 'min': 128, 'max': 4096}
        result = graphios.format_perfdata(pd)
        assert result.startswith("'free_mem'=1234MB;;;128;4096")

def test_public_split_perfdata():
    if hasattr(graphios, "split_perfdata"):
        perfdata = "'cpu'=15%;20;30;0;100 'mem'=4096MB;;;128;16384"
        pd_list = graphios.split_perfdata(perfdata)
        assert pd_list[1]['label'] == "mem"
        assert pd_list[1]['value'] == 4096
        assert pd_list[1]['uom'] == "MB"

def test_public_strip_perf_label():
    if hasattr(graphios, "strip_perf_label"):
        assert graphios.strip_perf_label("'swap'") == "swap"
        assert graphios.strip_perf_label("disk") == "disk"

def test_public_is_numeric():
    if hasattr(graphios, "is_numeric"):
        assert graphios.is_numeric("483.3")
        assert not graphios.is_numeric("test998")

def test_public_perfdata2list():
    if hasattr(graphios, "perfdata2list"):
        pd = "'io_read'=1MB 'io_write'=2MB;;;0;100"
        res = graphios.perfdata2list(pd)
        assert res[0]["label"] == "io_read"
        assert res[1]["label"] == "io_write"