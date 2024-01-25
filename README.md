# wolt_2024_delivery_fee_calc

This is a delivery fee calculator for Wolt API. 

The package consists of the next repos and modules:

  **x delivery** (contains all the modules, connected with the delivery fee calciulstion):
  
    - delivery_fee_calculation.py (all the classes and functions connected with the delivery fee calculation)
    
    - delivery_parameters.py (the default(constant) parameters you add for correct calculation and whicha are used in delivery_fee_calculation.py)
    
  **x TestApp** (containes all the unit tests)
  
    - test_corresponding.py
    
    - test_delivery_fee_calculation.py
    
    - test_error_scenarious.py
    
  **- app.py (API)**
  
  **- delivery_fee_generator** (contains abric-function to create a single calculation for a better async. processes' control)
