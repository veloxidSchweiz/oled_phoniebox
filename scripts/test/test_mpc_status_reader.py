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

    def test_get_info(self, status_reader):
        print()
        for k, v in status_reader.get_info().items():
            print(f'{k:<20}: {v}')
        pass

    def test_with_statement(self):
        with MPCStatusReader() as client:
            print(client.get_status())

    @pytest.mark.skip
    def test_has_messages(self):
        with MPCStatusReader() as client:
            client.has_messages()

    @pytest.mark.skip
    @pytest.mark.parametrize('msgs,expected,has_msgs',
                             [
                                 ([], None, False),
                                 (['hallo'], 'hallo', False),
                                 (['hallo', 'welt'], 'hallo', True),
                             ])
    def test_get_message(self, msgs, expected, has_msgs):
        with MPCStatusReader() as client:
            client.messages.extend(msgs)
            assert expected == client.get_message()
            assert has_msgs == client.has_messages()
