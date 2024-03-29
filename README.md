README
Delivery Fee Calculator
This program is designed to calculate delivery fees based on various factors such as cart value, number of items, order time, and delivery distance. It includes a comprehensive set of rules to determine the final delivery fee, considering surcharges for small orders, bulk items, and rush hour periods.

Features
Cart Value Analysis: Calculates delivery fees based on the total value of the cart.
Item Count Surcharges: Adds surcharges for orders with a large number of items.
Distance Calculation: Adjusts fees based on the delivery distance.
Rush Hour Pricing: Implements higher rates during Friday rush hours.
Maximum Fee Limitation: Ensures the delivery fee does not exceed a set maximum.
Free Delivery Threshold: Offers free delivery for high-value carts.

Setup

Install Dependencies:
In terminal, navigate to the project directory and install the required Python packages:

In terminal, run the following code:
pip install -r requirements.txt

---

To launch the app through the localhost run the following code in terminal: 

python app.py

For POST-requests' testing use Python Console:

whrite a JSON-request you want to test to console in form: 
{
    "cart_value": [int in cents],
    "number_of_items": [int],
    "order_time": "[2024-01-15T13:00:00Z]",
    "delivery_distance": [int in meters]
}

for example:

url = 'http://localhost:5000/calculate_fee'
data = {
    "cart_value": 70.00,
    "number_of_items": 1,
    "order_time": "2024-01-15T13:00:00Z",
    "delivery_distance": 50000
}

run the request and get the delivery fee in cents

----

Testing

To run the tests, write the following command to the terminal:
pytest

Ensure all tests are passing to verify the correct functionality of the program.

----

Development and Contribution

Linting: Ensure code follows PEP8 standards.
Testing: Add new tests for additional features or bug fixes.
Pull Requests: Submit a PR for proposed changes with a description of what the changes entail.
Contact
For any queries or contributions, please contact valeriiaskr@gmail.com (Valeriia Skripchenkova).

License
This project is licensed under the Valeriia Skripchenkova(c).

End of README.

----

You can customize this README file by adding additional sections as needed, such as 'Configuration', 'API Documentation', or 'Known Issues'. Remember to replace placeholders like valeriia-skr, valeriiaskr@gmail.com, and Valeriia Skripchenkova(c) with actual information.





