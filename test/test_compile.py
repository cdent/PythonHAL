

def test_compile():
    try:
        import hal
        assert True
    except ImportError, exc:
        assert False, exc
