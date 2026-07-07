# test/test_extension_registration.py

import importlib

from twip.verb import VERBS
from twip.extensions import load_extension


def test_importing_extension_module_does_not_register_verb(restore_verbs):
    importlib.import_module("twip_ext.pushable")

    assert "push" not in VERBS


def test_loading_extension_registers_verb(restore_verbs):
    load_extension("twip_ext.pushable")

    assert "push" in VERBS