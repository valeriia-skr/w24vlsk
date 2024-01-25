from flask import Flask, request, jsonify, logging
from datetime import datetime

import delivery_fee_generator
import logging

app = Flask(__name__)


@app.route('/calculate_fee', methods=['POST'])
def get_delivery_fee():
    try:
        data = request.get_json()
        cart_value = float(data['cart_value'])
        number_of_items = int(data['number_of_items'])
        order_time = datetime.strptime(data['order_time'], '%Y-%m-%d %H:%M:%S')
        delivery_distance = int(data['delivery_distance'])

        # Validation for invalid number_of_items
        if number_of_items < 0:
            raise ValueError("Number of items cannot be negative")

        # here we use a fabric-function to create a single calculation for a better async. processes' control
        new_delivery_fee_calculation = delivery_fee_generator.generate_new_delivery_fee_calculation()
        final_delivery_fee = new_delivery_fee_calculation.calculate_delivery_fee(cart_value,
                                                                                 number_of_items,
                                                                                 order_time,
                                                                                 delivery_distance
                                                                                 )

        return jsonify({"delivery_fee": final_delivery_fee})

    except ValueError as value_error:
        return jsonify({"error": f"Given value is incorrect: {value_error}"}), 400

    except KeyError as key_error:
        return jsonify({"error": f"Missing key value: {key_error}"}), 400

    except TypeError as type_error:
        return jsonify({"error": f"Incorrect data type: {type_error}"}), 400

    except Exception as e:
        # Log the full stack trace for developer analysis
        logging.error(f"Unhandled error: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)
