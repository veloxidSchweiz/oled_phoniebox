import pytest

from scripts.mpc_status_reader import MPCStatusReader


@pytest.fixture(scope="session")
def status_reader():
    return MPCStatusReader()

class TestMPCStatusReader:
    @pytest.mark.skipif(True, reason='ignore')
    def test_init(self):
        MPCStatusReader()
    @pytest.mark.skipif(True, reason='ignore')
    def test_get_status(self, status_reader):
        print(status_reader.get_status())

    def test_get_info(self,status_reader):
        print()
        for k,v in status_reader.get_info().items():
            print(f'{k:<20}: {v}')

    def test_with_statement(self):
        with MPCStatusReader() as client:
            print(client.get_status())