# This is alpha version and was used for testing the functionality of the code with tests from "delivery_fee_calculator_tests.py"
# You can test this calculator by pressing "Run Python File"

import json
from datetime import datetime, timedelta

def calculate_delivery_fee(json_input):

    try:
        input_data = json.loads(json_input)

        # Extract values from the input json
        cart_value = int(input_data["cart_value"])
        delivery_distance = int(input_data["delivery_distance"])
        number_of_items = int(input_data["number_of_items"])
        time = str(input_data["time"])

        # Rule 1: Calculate the small order surcharge if cart value is less than 10€
        minimum_cart_value = 1000
        small_order_surcharge = max(0, minimum_cart_value - cart_value)

        # Rule 2: Calculate the delivery fee based on the distance. Base fee is 2€ and 1€ is added for every 500 meters
        base_delivery_fee = 200
        additional_distance_fee = 100
        additional_distance_threshold = 500

        # Calculate the additional distance surcharge
        additional_distance_surcharge = max(
            0, ((delivery_distance - 1000 + additional_distance_threshold - 1) // additional_distance_threshold) * additional_distance_fee)

        # Make sure that the base delivery fee is always applied
        total_delivery_fee = base_delivery_fee + additional_distance_surcharge

        # Rule 3: Calculate the surcharge 0.5€/item when number of items is 5 or more. Also add bulk fee 1.2€ if the amount of items is over 12
        item_surcharge = 50
        bulk_fee_threshold = 12
        bulk_fee = 120
        total_item_surcharge = max(0, (number_of_items - 4) * item_surcharge)
        if number_of_items > bulk_fee_threshold:
            total_item_surcharge += bulk_fee

        # Calculate total delivery fee
        total_delivery_fee = small_order_surcharge + base_delivery_fee + \
            additional_distance_surcharge + total_item_surcharge

        # Rule 4: Check if the order is placed on Friday 3 - 7 PM and add 1.2x multiplier if needed
        order_time = datetime.fromisoformat(time)

        if order_time.weekday() == 4:
            rush_start_time = timedelta(hours = 15)
            rush_end_time = timedelta(hours = 19)

            current_time_today = timedelta(
                hours = order_time.hour, minutes = order_time.minute, seconds = order_time.second)

            if rush_start_time <= current_time_today <= rush_end_time:
                total_delivery_fee *= 1.2

                # Rule 5: Make sure that the delivery fee can not be over 15€
                max_delivery_fee = 1500
                total_delivery_fee = min(total_delivery_fee, max_delivery_fee)
        
        #Rule 6: Make sure that the delivery fee is 0€ if cart value is 200€ or more
        if cart_value >= 20000:
            total_delivery_fee = 0

        return total_delivery_fee
    
    except ValueError as e:
        # Re-raise the ValueError with a custom error message
        raise ValueError("Error: Invalid input. Check your input values.") from e

# Example use:
json_input = '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}'
delivery_fee = calculate_delivery_fee(json_input)
print(f'{{"delivery_fee": {delivery_fee}}}')