

def test_compile():
    try:
        import simplehal
        assert True
    except ImportError, exc:
        assert False, exc
