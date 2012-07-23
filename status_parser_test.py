import unittest
import mock
from status_parser import StatusParser

class StatusParserBaseTests(unittest.TestCase):

    def setUp(self):
        self.statuses = ["001001", "01010100", "1111"]
        team_list = []
        positions = []
        byte = ""
        self.sut_class = StatusParser
        self.sut = self.sut_class(self.statuses, team_list, positions, byte)

    def test_init_sets_statuses_in_constructor(self):
        sut = self.sut_class(self.statuses, mock.ANY, mock.ANY, mock.ANY)
        self.assertEqual(sut.statuses, self.statuses)

    def test_init_sets_team_list_in_constructor(self):
        sut = self.sut_class(mock.ANY, ['lol', 'eagles'], mock.ANY, mock.ANY)
        self.assertEqual(sut.team_list, ['lol', 'eagles'])

    def test_init_sets_positions_in_constructor(self):
        sut = self.sut_class(mock.ANY, mock.ANY, ['qb', 'rb'], mock.ANY)
        self.assertEqual(sut.positions, ['qb', 'rb'])

    def test_init_sets_byte_in_constructor(self):
        sut = self.sut_class(mock.ANY, mock.ANY, mock.ANY, "asdfsa")
        self.assertEqual(sut.file, "asdfsa")

    def test_pad_binary_strings_function_exists(self):
        with self.assertRaises(AssertionError):
            with self.assertRaises(AttributeError):
                self.sut.set_binary_strings()

    def test_pad_binary_string_function_exists(self):
        with self.assertRaises(AssertionError):
            with self.assertRaises(AttributeError):
                self.sut.pad_binary_string("")

    def test_set_condition_on_player_position_exists(self):
        with self.assertRaises(AssertionError):
            with self.assertRaises(AttributeError):
                self.sut.set_condition_on_player_position()

    def test_increment_byte_scanner_exists(self):
        with self.assertRaises(AssertionError):
            with self.assertRaises(AttributeError):
                self.sut.increment_byte_scanner(1, 2)

    def test_last_position_exists(self):
        with self.assertRaises(AssertionError):
            with self.assertRaises(AttributeError):
                self.sut.last_position(1)

    @mock.patch('status_parser.StatusParser.pad_binary_string')
    def test_set_binary_strings_calls_pad_binary_string_for_each_item_in_status_list(self, pad_binary_string):
        status_list = [mock.ANY, mock.ANY, mock.ANY]
        sut = self.sut_class(status_list, mock.ANY, mock.ANY, mock.ANY).set_binary_strings()
        self.assertEqual(pad_binary_string.call_count, len(status_list))

    @mock.patch('status_parser.StatusParser.pad_binary_string')
    def test_set_binary_strings_calls_pad_binary_string_with_args_for_each_item_in_list(self, pad_binary_string):
        status_list = ["larry", "curly", "moe"]
        sut = self.sut_class(status_list, mock.ANY, mock.ANY, mock.ANY).set_binary_strings()
        self.assertEqual(pad_binary_string.mock_calls[0], mock.call(status_list[0]))
        self.assertEqual(pad_binary_string.mock_calls[1], mock.call(status_list[1]))
        self.assertEqual(pad_binary_string.mock_calls[2], mock.call(status_list[2]))

    @mock.patch('status_parser.StatusParser.pad_binary_string')
    def test_set_binary_strings_sets_padded_binary_strings_to_instance_variable(self, pad_binary_string):
        status_list = ["larry", "curly", "moe"]
        sut = self.sut_class(status_list, mock.ANY, mock.ANY, mock.ANY)
        sut.set_binary_strings()
        for idx, status in enumerate(status_list):
            self.assertEqual(sut.binary_strings[idx], pad_binary_string.return_value)

    def test_pad_binary_string_returns_string_padded_with_zeros_if_len_less_than_8(self):
        expected = "00001111"
        actual = self.sut.pad_binary_string("1111")
        self.assertEqual(expected, actual)

    def test_pad_binary_string_returns_original_string_if_len_equal_to_8(self):
        expected = "00001111"
        actual = self.sut.pad_binary_string(expected)
        self.assertEqual(expected, actual)

    def test_last_position_returns_true_if_index_is_one_less_than_length_of_positions(self):
        self.sut.positions = [mock.ANY, mock.ANY, mock.ANY, mock.ANY]
        result = self.sut.last_position(3)
        self.assertTrue(result)

    def test_last_position_returns_false_if_index_is_not_one_less_than_length_of_positions(self):
        self.sut.positions = [mock.ANY, mock.ANY, mock.ANY, mock.ANY]
        result = self.sut.last_position(2)
        self.assertFalse(result)

    @mock.patch('status_parser.StatusParser.last_position')
    def test_increment_byte_scanner_increments_i_but_not_x_if_not_last_position(self, last_position):
        last_position.return_value = False
        i, x = self.sut.increment_byte_scanner(1, 2)
        self.assertEqual((2, 2), (i, x))

    @mock.patch('status_parser.StatusParser.last_position')
    def test_increment_byte_scanner_increments_x_and_sets_i_to_zero_if_last_position_and_x_not_one(self, last_position):
        original_x = 2
        last_position.return_value = True
        i, x = self.sut.increment_byte_scanner(mock.ANY, original_x)
        self.assertEqual((0, original_x + 1), (i, x))

    @mock.patch('status_parser.StatusParser.last_position')
    def test_increment_byte_scanner_returns_zero_and_x_if_last_position_and_x_is_one(self, last_position):
        last_position.return_value = True
        i, x = self.sut.increment_byte_scanner(1, 1)
        self.assertEqual((0, 1), (i, x))

class StatusParserSetConditionOnPlayerPositionTests(unittest.TestCase):

    def setUp(self):
        self.statuses = ["001001", "01010100", "1111"]
        team_list = []
        positions = []
        byte = ""
        self.sut_class = StatusParser
        self.sut = self.sut_class(self.statuses, team_list, positions, byte)

    #freakin punting on this