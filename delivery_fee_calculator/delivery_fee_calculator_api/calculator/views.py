from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from .values import (
    MINIMUM_CART_VALUE,
    BASE_DELIVERY_FEE,
    ADDITIONAL_DISTANCE_FEE,
    ADDITIONAL_DISTANCE_THRESHOLD,
    ITEM_SURCHARGE,
    BULK_FEE_THRESHOLD,
    BULK_FEE,
    MAX_DELIVERY_FEE,
    CART_VALUE_THRESHOLD,
    RUSH_START_TIME,
    RUSH_END_TIME,
)
# Exempt this part from CSRF protection to avoid "CSRF verification failed" error.
@csrf_exempt
def calculate_delivery_fee(request):
    if request.method == 'POST':
        try:
            input_data = json.loads(request.body)

            # Extract values from the input json
            cart_value = int(input_data["cart_value"])
            delivery_distance = int(input_data["delivery_distance"])
            number_of_items = int(input_data["number_of_items"])
            time = str(input_data["time"])

            # Rule 1: Calculate the small order surcharge if cart value is less than 10€
            minimum_cart_value = MINIMUM_CART_VALUE
            small_order_surcharge = max(0, minimum_cart_value - cart_value)

            # Rule 2: Calculate the delivery fee based on the distance. Base fee is 2€ and 1€ is added for every 500 meters
            base_delivery_fee = BASE_DELIVERY_FEE
            additional_distance_fee = ADDITIONAL_DISTANCE_FEE
            additional_distance_threshold = ADDITIONAL_DISTANCE_THRESHOLD

            # Calculate the additional distance surcharge
            additional_distance_surcharge = max(
                0, ((delivery_distance - 1000 + additional_distance_threshold - 1) // additional_distance_threshold) * additional_distance_fee)

            # Make sure that the base delivery fee is always applied
            total_delivery_fee = base_delivery_fee + additional_distance_surcharge

            # Rule 3: Calculate the surcharge 0.5€/item when number of items is 5 or more. Also add bulk fee 1.2€ if the amount of items is over 12
            item_surcharge = ITEM_SURCHARGE
            bulk_fee_threshold = BULK_FEE_THRESHOLD
            bulk_fee = BULK_FEE
            total_item_surcharge = max(0, (number_of_items - 4) * item_surcharge)
            if number_of_items > bulk_fee_threshold:
                total_item_surcharge += bulk_fee

            # Calculate total delivery fee
            total_delivery_fee = small_order_surcharge + base_delivery_fee + additional_distance_surcharge + total_item_surcharge

            # Rule 4: Make sure that the delivery fee is 0€ when cart value is 200€ or more
            if cart_value >= CART_VALUE_THRESHOLD:
                total_delivery_fee = 0

            # Rule 5: Check if the order is placed on Friday 3 - 7 PM and add a 1.2x multiplier if needed
            order_time = datetime.fromisoformat(time)

            if order_time.weekday() == 4:
                rush_start_time = RUSH_START_TIME
                rush_end_time = RUSH_END_TIME

                current_time_today = timedelta(hours=order_time.hour, minutes=order_time.minute, seconds=order_time.second)

                if rush_start_time <= current_time_today <= rush_end_time:
                    total_delivery_fee *= 1.2

                    # Rule 6: Make sure that the delivery fee won't exceed 15€
                    max_delivery_fee = MAX_DELIVERY_FEE
                    total_delivery_fee = min(total_delivery_fee, max_delivery_fee)
                    delivery_fee = int(total_delivery_fee)
            else:
                delivery_fee = total_delivery_fee

            # Return the calculated delivery fee in json
            return JsonResponse({"delivery_fee": delivery_fee})
        
        # Return an error if payload contains invalid input
        except ValueError as e:
            return JsonResponse({"error": "Invalid input. Check your input values."}, status=400)
        
    # Return an error if the incoming request's method is not POST
    return JsonResponse({"error": "Method Not Allowed"}, status=405)
