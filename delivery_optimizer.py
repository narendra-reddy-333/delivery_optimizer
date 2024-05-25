import math
import logging
from itertools import permutations
from typing import List, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Geolocation:
    """Represents a geographic location with latitude and longitude."""

    def __init__(self, latitude: float, longitude: float):
        """Initializes a Geolocation object.

        Args:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.

        Raises:
            ValueError: If latitude or longitude are not within valid ranges.
        """
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees.")

        self.latitude = latitude
        self.longitude = longitude


class DeliveryOptimizer:
    """Optimizes delivery routes for a delivery executive."""

    def __init__(self, average_speed: int = 20):
        """Initializes DeliveryOptimizer with an average speed.

        Args:
            average_speed (int, optional): Average speed in km/hr. Defaults to 20.
        """
        if average_speed <= 0:
            raise ValueError("Average speed must be a positive value.")

        self.average_speed = average_speed
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def haversine_distance(location1: Geolocation, location2: Geolocation) -> float:
        """Calculates the distance between two Geolocation objects using the Haversine formula.

        Args:
            location1 (Geolocation): The first geolocation.
            location2 (Geolocation): The second geolocation.

        Returns:
            float: The distance between the two locations in kilometers.
        """

        R = 6371  # Radius of Earth in kilometers
        lat1 = math.radians(location1.latitude)
        lon1 = math.radians(location1.longitude)
        lat2 = math.radians(location2.latitude)
        lon2 = math.radians(location2.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    def calculate_travel_time(self, location1: Geolocation, location2: Geolocation) -> float:
        """Calculates the travel time between two locations.

        Args:
            location1 (Geolocation): The starting location.
            location2 (Geolocation): The destination location.

        Returns:
            float: The travel time in minutes.
        """

        distance = self.haversine_distance(location1, location2)
        travel_time_hours = distance / self.average_speed
        travel_time_minutes = travel_time_hours * 60
        return travel_time_minutes

    @staticmethod
    def generate_routes(r1_location: Geolocation, c1_location: Geolocation,
                        r2_location: Geolocation, c2_location: Geolocation) -> List[List[Geolocation]]:
        """Generates all possible delivery routes.

        Args:
            r1_location (Geolocation): Location of restaurant 1.
            c1_location (Geolocation): Location of consumer 1.
            r2_location (Geolocation): Location of restaurant 2.
            c2_location (Geolocation): Location of consumer 2.

        Returns:
            List[List[Geolocation]]: A list of possible routes, each a list of Geolocation objects.
        """

        locations = [r1_location, c1_location, r2_location, c2_location]
        routes = list(permutations(locations))  # Use permutations to generate routes

        return [list(route) for route in routes]  # Convert tuples to lists

    def calculate_route_time(
            self, route: List[Geolocation], aman_location: Geolocation, pt1: int, pt2: int) -> float:
        """Calculates the total time for a given route.

        Args:
            route (List[Geolocation]): A list of Geolocation objects representing the route.
            aman_location (Geolocation): Aman's starting location.
            pt1 (int): Preparation time at restaurant 1 (in minutes).
            pt2 (int): Preparation time at restaurant 2 (in minutes).

        Returns:
            float: The total time for the route in minutes.
        """

        if pt1 < 0 or pt2 < 0:
            raise ValueError("Preparation times must be non-negative values.")

        total_time = 0
        current_location = aman_location

        for i, location in enumerate(route):
            travel_time = self.calculate_travel_time(current_location, location)
            total_time += travel_time

            # Add waiting time at the restaurant (assuming restaurants are at indices 0 and 2)
            if i == 0 or i == 2:
                if location.latitude == r1_location.latitude and location.longitude == r1_location.longitude:
                    total_time += pt1
                elif location.latitude == r2_location.latitude and location.longitude == r2_location.longitude:
                    total_time += pt2

            current_location = location

        return total_time

    def find_best_route(
            self, aman_location: Geolocation, r1_location: Geolocation, c1_location: Geolocation,
            r2_location: Geolocation, c2_location: Geolocation, pt1: int, pt2: int) -> Tuple[List[Geolocation], float]:
        """Finds the best delivery route and estimated time.

        Args:
            aman_location (Geolocation): Aman's location.
            r1_location (Geolocation): Restaurant 1 location.
            c1_location (Geolocation): Customer 1 location.
            r2_location (Geolocation): Restaurant 2 location.
            c2_location (Geolocation): Customer 2 location.
            pt1 (int): Preparation time at restaurant 1.
            pt2 (int): Preparation time at restaurant 2.

        Returns:
            Tuple[List[Geolocation], float]: The best route (list of Geolocations) and minimum time (float).
        """

        best_route = None
        min_time = float('inf')

        for route in self.generate_routes(r1_location, c1_location, r2_location, c2_location):
            try:
                route_time = self.calculate_route_time(route, aman_location, pt1, pt2)
                if route_time < min_time:
                    min_time = route_time
                    best_route = route
            except ValueError as e:
                self.logger.error(f"Error calculating route time: {e}")

        if best_route is None:
            self.logger.error("Could not find a valid route.")
            raise ValueError("No valid route found.")

        return best_route, min_time


# Example Usage
if __name__ == "__main__":
    optimizer = DeliveryOptimizer()

    try:
        aman_location = Geolocation(12.97, 77.59)
        r1_location = Geolocation(12.93, 77.62)
        r2_location = Geolocation(12.99, 77.65)
        c1_location = Geolocation(13.01, 77.68)
        c2_location = Geolocation(12.95, 77.55)
        pt1 = 15
        pt2 = 10

        best_route, min_time = optimizer.find_best_route(
            aman_location, r1_location, c1_location,
            r2_location, c2_location, pt1, pt2
        )

        print("Best Route:")
        for location in best_route:
            print(f"  Latitude: {location.latitude}, Longitude: {location.longitude}")

        print(f"Estimated Time (minutes): {min_time:.2f}")

    except ValueError as e:
        print(f"Error: {e}")
