import unittest
from mqtt import clients


class TestPublisher(unittest.TestCase):

    def setUpClass(self):
        connect_data = {
             "topic": "temperature_inside",
             "broker": "localhost",
             "client_name": "temperature_inside"
        }

        self.publisher = clients.Publisher(**connect_data)

    def test_if_publisher_is_connected_after_ack_rc_is_0(self):  # test to check connection to broker
        self.publisher.on_connect("a", "b", "c", 0)
        self.assertEqual(0, self.publisher.connected)


if __name__ == "__main__":
    unittest.main()
