# Delivery Route Optimizer

## Description

This Python script provides a solution for optimizing delivery routes for a delivery executive who needs to pick up orders from restaurants and deliver them to customers in the shortest possible time. It uses the Haversine formula to calculate travel time between locations and considers the preparation time at each restaurant.

## Features

- **Route Optimization:** Calculates the optimal delivery route for two orders, minimizing the total delivery time.
- **Permutations:** Uses the `itertools.permutations` function to efficiently generate all possible routes.
- **Haversine Formula:**  Accurately calculates distances between geographic locations, taking into account the curvature of the Earth.
- **Preparation Time:**  Includes the restaurant preparation time in the route time calculation.
- **Error Handling:**  Handles invalid inputs and potential errors during calculation.
- **Logging:**  Logs important events and errors for debugging and monitoring.
- **Type Hints:**  Uses type hints for improved code readability and static analysis.

## Requirements

- Python 3.6 or higher

## Usage

1. **Input Data:**
   - Provide the latitude and longitude for:
     - Aman's current location
     - Restaurant 1 location
     - Restaurant 2 location
     - Consumer 1 location
     - Consumer 2 location
   - Specify the average preparation times (`pt1` and `pt2`) for the two restaurants in minutes.

2. **Run the Script:**
   - Execute the script using `python delivery_optimizer.py` (replace `delivery_optimizer.py` with the actual filename).

3. **Output:**
   - The script will print:
     - The best route (sequence of locations).
     - The estimated total time for the best route in minutes.

## Future Improvements

- **More Orders:** Extend the algorithm to handle more than two orders.
- **Multiple Drivers:** Optimize routes for multiple delivery executives.
- **Time Windows:**  Consider time windows for pickup and delivery.
- **Real-time Traffic Data:**  Integrate real-time traffic data for more accurate time estimations.
- **API Integration:**  Connect to external APIs for location services, restaurant order information, and driver communication.
