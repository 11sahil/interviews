BEST ROUTE

**Question Refrence**

![image](https://github.com/11sahil/interviews/assets/37617943/18cb0efb-4914-4ff4-9a65-4845cec18c3d)


Imagine a delivery executive called Aman standing idle in Koramangala somewhere when suddenly his
phone rings and notifies that he’s just been assigned a batch of 2 orders meant to be delivered in the
shortest possible timeframe.
All the circles in the figure above represent geo-locations :
● C1 : Consumer 1
● C2 : Consumer 2
● R1 : Restaurant C1 has ordered from. Average time it takesto prepare a meal is pt1
R2 : Restaurant C2 has ordered from. Average time it takes to prepare a meal is pt2
Since there are multiple ways to go about delivering these orders, your task is to help Aman figure out
the best way to finish the batch in the shortest possible time.
For the sake of simplicity, you can assume that Aman, R1 and R2 were informed about these orders at
the exact same time and all of them confirm on doing it immediately. Also, for travel time between
any two geo-locations, you can use the haversine formula with an average speed of 20km/hr (
basically ignore actual road distance or confirmation delays everywhere although the real world is
hardly that simple ;) )
Note: Code should be of production quality and should take into consideration the best practices of
the language chosen

**Assumtions**
Each resturant will have only one order from one user


**Approach**

Approach we have taken here is kind of greedy where in we start with agent look for smallest time to be taken for first
and then smallest time to be taken for nearest resturant or customers 

Also we have taken consideration of time taken by resturant to prepare food and meanwhile when agent drives to that location
The final print value shows what route can agent take for its optimized journey

I have created one service layer For the sake of simplicity I have kept all service class in single file we can easily seprate them out going forward
I have created one repository layer for mimicing DB
If in future we have to introdcue DB we have to just change the implementation within repository layer

