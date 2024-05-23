import math
import datetime
from repository import userRepository, restaurantRepository, orderRepository

class userService:
    def __init__(self):
        self._user_repo = userRepository()

    def addUser(self, name, email, is_staff=False, is_superuser=False):
        try:
            return self._user_repo.addUser(name, email, is_staff, is_superuser)
        except Exception as e:
            print("Exception", e)

    def getUser(self, user_id):
        try:
            return self._user_repo.getUser(user_id)
        except Exception as e:
            print("Exception", e)

class restaurantService:
    def __init__(self):
        self._restaurant_repo = restaurantRepository()

    def addRestaurant(self, name, address, average_time, lat, lng):
        try:
            return self._restaurant_repo.addRestaurant(name, address, average_time, lat, lng)
        except Exception as e:
            print("Exception", e)

    def getRestaurant(self, restaurant_id):
        try:
            return self._restaurant_repo.getRestaurant(restaurant_id)
        except Exception as e:
            print("Exception", e)


class orderService:
    def __init__(self):
        self._order_repo = orderRepository()

    def addOrder(self, user_id, restaurant_id, user_lat, user_lng):
        try:
            time = datetime.datetime.now()
            return self._order_repo.addOrder(user_id, restaurant_id, time, user_lat, user_lng)
        except Exception as e:
            print("addOrder Exception", e)

    def getOrder(self, order_id):
        try:
            return self._order_repo.getOrder(order_id)
        except Exception as e:
            print("Exception", e)

    def getbulkOrder(self, order_id_list):
        try:
            return self._order_repo.getbulkOrder(order_id_list)
        except Exception as e:
            print("Exception", e)


class routeService:
    def __init__(self, user_service, resturant_service, order_service):
        self._user_service = user_service
        self._restaurant_service = resturant_service
        self._order_service = order_service
        self.position_map = {}
        self.resturants = set()
        self.customers = set()
    
    @classmethod
    def calculate_ditance_bw_two_points(cls, lat1, lon1, lat2, lon2):
        R = 6371
        dLat = (lat2 - lat1) * math.pi/180
        dLon = (lon2 - lon1) * math.pi/180
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi/180) * math.cos(lat2 * math.pi/180) * math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
        d = R * c
        return d

    def getBestRoute(self, agent_id, agent_lat, agent_lng, orders_list=[]):
        if not orders_list:
            return None
        agent = self._user_service.getUser(agent_id)
        if agent is None:
            return None
        orders = self._order_service.getbulkOrder(orders_list) 
        if orders is None:

            return None
        graph = self.build_graph(orders, agent_id, agent_lat, agent_lng)
        delivery_route = self.calculate_shortest_path(graph, orders, agent_id)
        return delivery_route
    
    def build_graph(self, orders, agent_id, agent_lat, agent_lng):
        graph = {}
        self.position_map["U_"+str(agent_id)] = (agent_lat, agent_lng)
        for each_order in orders:
            resturant_id="R_"+str(each_order.get("restaurant_id"))
            resturant = self._restaurant_service.getRestaurant(each_order.get("restaurant_id"))
            user_id="U_"+str(each_order.get("user_id"))
            if resturant_id not in graph:
                graph[resturant_id] = {}

            graph[resturant_id][user_id] = self.calculate_ditance_bw_two_points(resturant.get("lat"), resturant.get("lng"), each_order.get("lat"), each_order.get("lng"))
            graph[resturant_id]["U_"+str(agent_id)] = self.calculate_ditance_bw_two_points(resturant.get("lat"), resturant.get("lng"), agent_lat, agent_lng)
            self.resturants.add(resturant_id)
            self.customers.add(user_id)
            if resturant_id not in self.position_map:
                self.position_map[resturant_id] = (resturant.get("lat"), resturant.get("lng"))
            if user_id not in self.position_map:
                self.position_map[user_id] = (each_order.get("lat"), each_order.get("lng"))
        return graph

    def get_distance_from_graph(self, graph, origin, destination):
        dist=None
        if origin in graph:
            if destination in graph[origin]:
                dist = graph[origin][destination]
        elif destination in graph:
            if origin in graph[destination]:
                dist = graph[destination][origin]
        if not dist:
            dist = self.calculate_ditance_bw_two_points(self.position_map[origin][0], 
                                                        self.position_map[origin][1], 
                                                        self.position_map[destination][0], 
                                                        self.position_map[destination][1])
            if origin not in graph:
                graph[origin]={destination: dist}
            else:
                graph[origin][destination] = dist
        return dist
        
    def get_customer_for_resturant(self, orders, node):
        resturant_id = int(node.replace("R_", ""))
        for each_order in orders:
            if each_order.get("restaurant_id") == resturant_id:
                return each_order.get("user_id")
            
    def get_average_time_for_resturant(self, orders, node):
        resturant_id = int(node.replace("R_", ""))
        for each_order in orders:
            if each_order.get("restaurant_id") == resturant_id:
                resturant = self._restaurant_service.getRestaurant(each_order.get("restaurant_id"))
                return resturant.get("average_time")
    
    def calculate_shortest_path(self, graph, orders, agent_id, average_speed=20):
        origin = "U_"+str(agent_id)
        total_orders = len(orders)
        next_nodes = list(self.resturants)
        order_delivered = []
        orders_picked_up = []
        delivery_route = []
        distance_traveled_so_far = 0
        while len(order_delivered) != total_orders:
            comparison_map = {}
            for node in next_nodes:
                distance_to_reach = self.get_distance_from_graph(graph, origin, node)
                time_to_reach = distance_to_reach / average_speed
                time_complted_so_far = distance_traveled_so_far / average_speed
                if node in self.resturants:
                    avg_time = self.get_average_time_for_resturant(orders, node)
                    if time_to_reach+ time_complted_so_far > avg_time:
                        comparison_map[node] = time_to_reach
                    else:
                        diff = avg_time - (time_to_reach+ time_complted_so_far)
                        comparison_map[node] = time_to_reach + diff
                else:
                    comparison_map[node] = time_to_reach
            selected_node = min(comparison_map, key=comparison_map.get)
            next_nodes.remove(selected_node)
            if selected_node in self.customers:
                order_delivered.append(selected_node)
            elif selected_node in self.resturants:
                orders_picked_up.append(selected_node)
                customer_id = self.get_customer_for_resturant(orders, selected_node)
                next_nodes.append("U_"+str(customer_id))
            delivery_route.append(selected_node)
            distance_traveled_so_far += self.get_distance_from_graph(graph, origin, selected_node)
            origin = selected_node
        return delivery_route
    
        

        
        


        