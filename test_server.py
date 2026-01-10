import unittest
from unittest.mock import MagicMock
from server import parse_suds_methods

class TestParseSudsMethods(unittest.TestCase):
    def test_parse_suds_methods(self):
        # Mock the suds Client structure
        mock_client = MagicMock()
        
        # Mock ServiceDefinition
        mock_sd = MagicMock()
        
        # Mock xlate method
        # We can make it return "xs:string" or something based on input
        def xlate_side_effect(arg_type):
            return "xs:string" if arg_type == "mock_string_type" else "xs:int"
        
        mock_sd.xlate.side_effect = xlate_side_effect
        
        # Define methods structure:
        # (method_name, list_of_args)
        # list_of_args: (arg_name, arg_type_obj)
        methods = [
            ("GetData", [("id", "mock_int_type"), ("name", "mock_string_type")]),
            ("DeleteData", [("id", "mock_int_type")])
        ]
        
        # Define ports structure:
        # (PortObject, methods_list)
        mock_port = MagicMock()
        ports = [
            (mock_port, methods)
        ]
        
        mock_sd.ports = ports
        mock_client.sd = [mock_sd]
        
        # Run the function
        result = parse_suds_methods(mock_client)
        
        # Verify results
        expected = {
            "GetData": [
                {"name": "id", "type": "xs:int"},
                {"name": "name", "type": "xs:string"}
            ],
            "DeleteData": [
                {"name": "id", "type": "xs:int"}
            ]
        }
        
        self.assertEqual(result, expected)
        
        # Verify xlate was called
        mock_sd.xlate.assert_any_call("mock_int_type")
        mock_sd.xlate.assert_any_call("mock_string_type")

if __name__ == '__main__':
    unittest.main()
