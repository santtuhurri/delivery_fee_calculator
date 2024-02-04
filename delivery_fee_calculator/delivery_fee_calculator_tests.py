# This file runs tests to test the functionality of "delivery_fee_calculator.py"

import unittest, timeit
from delivery_fee_calculator import calculate_delivery_fee

# Test 0 - Test the performance and the efficiency of code
def performance_test():
    # Define a sample input for the performance test
    json_input = '{"cart_value": 980, "delivery_distance": 2235, "number_of_items": 18, "time": "2024-01-15T13:00:00Z"}'

    # Measure the execution time of "calculate_delivery_fee"
    execution_time = timeit.timeit(lambda: calculate_delivery_fee(json_input), number=1000)

    # Print the average execution time per call
    print(f"Avg. Execution Time: {execution_time / 1000:.6f} seconds")

if __name__ == '__main__':
    performance_test()

class TestDeliveryFeeCalculation(unittest.TestCase):
    # Test 1 - Test that delivery fee is 2€, when distance is less than 1000 meters. No additional fee should be added
    def test_delivery_fee_short_distance(self):
        # Define a sample input for the performance test
        json_input ='{"cart_value": 1000, "delivery_distance": 200, "number_of_items": 3, "time": "2024-01-15T13:00:00Z"}'

        # Define a pre-calculated amount that is expected to be returned by the code
        expected_delivery_fee = 200

        # Run the code
        actual_delivery_fee = calculate_delivery_fee(json_input)

        # Check if the expected amount matches the amount calculated by the code
        self.assertEqual(round(actual_delivery_fee, 2), round(expected_delivery_fee, 2))

    # Test 2 - Test that correct surcharge is added when the cart value is less than 10€
    def test_delivery_distance_surcharge(self):
        json_input ='{"cart_value": 500, "delivery_distance": 200, "number_of_items": 3, "time": "2024-01-15T13:00:00Z"}'

        expected_delivery_fee = 700

        actual_delivery_fee = calculate_delivery_fee(json_input)
        self.assertEqual(round(actual_delivery_fee, 2), round(expected_delivery_fee, 2))    

    # Test 3 - Test that bulk fee is added correctly when there are over 12 items
    def test_delivery_fee_bulk(self):
        json_input ='{"cart_value": 500, "delivery_distance": 200, "number_of_items": 14, "time": "2024-01-15T13:00:00Z"}'

        expected_delivery_fee = 1320

        actual_delivery_fee = calculate_delivery_fee(json_input)
        self.assertEqual(round(actual_delivery_fee, 2), round(expected_delivery_fee, 2))  

    # Test 4 - Test that bulk fee is NOT added when there are exactly 12 items
    def test_delivery_fee_bulk_equal(self):
        json_input ='{"cart_value": 500, "delivery_distance": 200, "number_of_items": 12, "time": "2024-01-15T13:00:00Z"}'

        expected_delivery_fee = 1100

        actual_delivery_fee = calculate_delivery_fee(json_input)
        self.assertEqual(round(actual_delivery_fee, 2), round(expected_delivery_fee, 2))  

    # Test 5 - Test that Friday rush multiplier 1.2x is applied correctly
    def test_delivery_fee_rush_time(self):
        json_input ='{"cart_value": 500, "delivery_distance": 200, "number_of_items": 14, "time": "2024-01-26T18:00:00Z"}'

        expected_delivery_fee = 1500

        actual_delivery_fee = calculate_delivery_fee(json_input)
        self.assertEqual(round(actual_delivery_fee, 2), round(expected_delivery_fee, 2))      

    # Test 6 - Test that no surcharge is added to order over 10€
    def test_delivery_fee_no_surcharge(self):
        json_input = '{"cart_value": 2000, "delivery_distance": 1200, "number_of_items": 3, "time": "2024-01-15T13:00:00Z"}'
        
        expected_delivery_fee = 300
        
        actual_delivery_fee = calculate_delivery_fee(json_input)
        self.assertEqual(round(actual_delivery_fee, 2), round(expected_delivery_fee, 2))

    # Test 7 - Test that delivery fee is 0€, when cart value is 200€ or over
    def test_delivery_fee_free(self):
        json_input = '{"cart_value": 20000, "delivery_distance": 1200, "number_of_items": 3, "time": "2024-01-26T16:30:00Z"}'
      
        expected_delivery_fee = 0
        
        actual_delivery_fee = calculate_delivery_fee(json_input)
        self.assertEqual(round(actual_delivery_fee, 2), round(expected_delivery_fee, 2))

    # Test 9 - Test that long distance correctly adds +1€ for each 500 meters
    def test_delivery_fee_long_distance(self):
        json_input = '{"cart_value": 900, "delivery_distance": 3501, "number_of_items": 3, "time": "2024-01-28T16:30:00Z"}'
      
        expected_delivery_fee = 900
        
        actual_delivery_fee = calculate_delivery_fee(json_input)
        self.assertEqual(round(actual_delivery_fee, 2), round(expected_delivery_fee, 2))
        
    # Test 10 - Test that invalid inputs are handles correctly
class TestCalculateDeliveryFeeErrors(unittest.TestCase):
    def test_invalid_cart_value(self):
        json_input = '{"cart_value": "ERROR", "delivery_distance": 2000, "number_of_items": 200, "time": "2024-01-15T13:00:00Z"}'
        
        # Use assertRaises to check if a ValueError is raised
        with self.assertRaises(ValueError) as context:
            calculate_delivery_fee(json_input)
        
        # Check the error message
        self.assertEqual(str(context.exception), "Error: Invalid input. Check your input values.")

if __name__ == '__main__':
    unittest.main()

