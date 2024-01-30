from flask import Flask, request, jsonify, logging
from datetime import datetime
from validation import validate_data, validate_order_time

import delivery_fee_creator

app = Flask(__name__)


@app.route('/calculate_fee', methods=['POST'])
def get_delivery_fee():
    try:
        data = request.get_json()
        cart_value = data['cart_value']
        number_of_items = data['number_of_items']
        order_time = datetime.strptime(data['order_time'], '%Y-%m-%dT%H:%M:%SZ')
        delivery_distance = data['delivery_distance']

        # Check if the values are integers (or can be converted to integers without loss of information)
        validate_data(cart_value, "Cart value", int, can_be_zero=False)
        validate_data(number_of_items, "Number of items", int, can_be_zero=False)
        validate_data(delivery_distance, "Delivery distance", int, can_be_zero=False)

        validate_order_time(order_time)

        # here we use a fabric-function to create a single calculation for a better async. processes' control
        new_delivery_fee = delivery_fee_creator.create_new_delivery_fee()
        calculated_delivery_fee = new_delivery_fee.calculate(cart_value,
                                                             number_of_items,
                                                             order_time,
                                                             delivery_distance
                                                             )

        return jsonify({"delivery_fee": calculated_delivery_fee})

    except ValueError as value_error:
        return jsonify({"error": f"Given value is incorrect: {value_error}"}), 400

    except KeyError as key_error:
        return jsonify({"error": f"Missing key value: {key_error}"}), 400

    except TypeError as type_error:

        return jsonify({"error": f"Incorrect data type: {type_error}"}), 400

    except Exception as e:
        # Log the full stack trace for developer analysis
        logging.error(f"Unhandled error: {e}. Request details: "
                      f"{request.url}, "
                      f"{request.method}, "
                      f"{request.headers}, "
                      f"{request.get_data(as_text=True)}")
        return jsonify({"error": "An internal server error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)
