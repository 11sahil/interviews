import logging
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    
    def __init__(self):
        self.data={}
        self.id=0


class userRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def addUser(self, name, email, is_staff, is_superuser):
        self.id+=1
        self.data[self.id]={"name": name, "email": email, "is_staff": is_staff, "is_superuser": is_superuser, "is_active": True}
        return self.id
    
    def getUser(self, user_id):
        if user_id in self.data:
            return self.data[user_id]
        else:
            raise Exception("User not found")

class restaurantRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def addRestaurant(self, name, address, average_time, lat, lng):
        self.id+=1
        self.data[self.id]={"name": name, "lat": lat, "lng": lng, "average_time": average_time, "address": address , "available": True}
        return self.id
    
    def getRestaurant(self, restaurant_id):
        if restaurant_id in self.data:
            return self.data[restaurant_id]
        else:
            raise Exception("Restaurant not found")
    
    def updateRestaurant(self, restaurant_id, name, address, average_time, available):
        if restaurant_id in self.data:
            self.data[restaurant_id]["name"] = name
            self.data[restaurant_id]["address"] = address
            self.data[restaurant_id]["average_time"] = average_time
            self.data[restaurant_id]["available"] = available
            return self.data[restaurant_id]
        else:
            raise Exception("Restaurant not found")
        

class orderRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def addOrder(self, user_id, restaurant_id, time, lat, lng):
        self.id+=1
        self.data[self.id]={"user_id": user_id, "restaurant_id": restaurant_id, "order_time": time, "lat": lat, "lng": lng}
        return self.id

    def getOrder(self, order_id):
        if order_id in self.data:
            return self.data[order_id]
        else:
            raise Exception("Order not found")
        
    def getbulkOrder(self, order_id_list):
        orders = []
        for order_id in order_id_list:
            if order_id not in self.data:
                # would prefer here to use logger.error in production
                print("ERROR: Order not found")    
            orders.append(self.data[order_id]) 
        return orders

    def updateOrder(self, order_id, key, value):
        if order_id in self.data:
            self.data[order_id][key] = value
            return self.data[order_id]
        else:
            raise Exception("Order not found")