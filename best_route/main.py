import math
# Imagine a delivery executive called Aman standing idle in Koramangala somewhere when suddenly his
# phone rings and notifies that he’s just been assigned a batch of 2 orders meant to be delivered in the
# shortest possible timeframe.
# All the circles in the figure above represent geo-locations :
# ● C1 : Consumer 1
# ● C2 : Consumer 2
# ● R1 : Restaurant C1 has ordered from. Average time it takesto prepare a meal is pt1
# R2 : Restaurant C2 has ordered from. Average time it takes to prepare a meal is pt2
# Since there are multiple ways to go about delivering these orders, your task is to help Aman figure out
# the best way to finish the batch in the shortest possible time.
# For the sake of simplicity, you can assume that Aman, R1 and R2 were informed about these orders at
# the exact same time and all of them confirm on doing it immediately. Also, for travel time between
# any two geo-locations, you can use the haversine formula with an average speed of 20km/hr (
# basically ignore actual road distance or confirmation delays everywhere although the real world is
# hardly that simple ;) )

from service import orderService, restaurantService, routeService, userService

user_service = userService()
order_service = orderService()
restaurant_service = restaurantService()
route_service = routeService(user_service=user_service, order_service=order_service, resturant_service=restaurant_service)

u1 = user_service.addUser("Aman", "a@a.com")
u2 = user_service.addUser("Sahil", "s@s.com")
agent = user_service.addUser("Agent", "a@a.com", is_staff=True)

r1 = restaurant_service.addRestaurant("C1", "R1", 10, 12.9716, 77.5946)
r2 = restaurant_service.addRestaurant("C2", "R2", 15, 12.1976, 77.6)

o1 = order_service.addOrder(u1, r1, 12.9716, 77.5946)
o2 = order_service.addOrder(u2, r2, 12.1976, 77.6)
route = route_service.getBestRoute(agent, 19.9886, 73.59, [o1, o2])
print("RESULT: ","->".join(route))

