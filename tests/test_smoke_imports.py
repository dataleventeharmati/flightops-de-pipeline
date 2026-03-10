from __future__ import annotations

import importlib


def test_core_modules_import():
    modules = [
        "flightops",
        "flightops.fetch_states",
        "flightops.build_silver",
        "flightops.kpi_report",
        "flightops.region_kpi_report",
    ]
    for module_name in modules:
        module = importlib.import_module(module_name)
        assert module is not None
