# test/test_extensions_public_api.py

from twip.extensions import load_extension, load_extensions


def test_extensions_public_api_exports_loader_functions():
    assert load_extension
    assert load_extensions