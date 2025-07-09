# CSC172_05

Ethan Chang <br />
echang28@u.rochester.edu

CSC 172 Summer 2024
Lab 5: Street Mapping

Input files should be of the following form: <br/>
**For Intersections** i IntersectionID Latitude Longitude <br/>
**For Roads** r RoadID Intersection1ID Intersection2ID

This lab and code are meant to create a basic mapping program using Java. When coding this, I first looked to define the key elements needed: the node and the edge. I then used these two elements to represent a graph by storing the data of a node and its edges. Adding each node and edge is executed on O(1) time, as it just inserts one piece of information each time it is called. After figuring out how to implement those, I began working on Dijkstra's algorithm and how to find the MST. For Dijksstra's, initializing takes O(V) time, requiring it to look through all the nodes. A priority queue was used, and since each node updates it and the node's edges, it results in an O((V+E)logV) time complexity. As such, Dijkstra takes O((V+E)logV) as it is the dominant term. MST was implemented using a priority queue for the edges, leading to each edge being initiated and O(E). It then processes the path by looking at each edge, leading to O((V+E)logE) time complexity. As such, MST is O((V+E)logE). To show the image representation of the graph, each node and graph must be observed, leading to O(V+E) time complexity. As such, even when dealing with large data sets, my code will largely be able to hold up as these time complexities perform fairly well with scalability.

Examples from the Data Structures and Algorithms zyBook by Roman Lysecky and Frank Vahid were referenced when writing this code. 

List of file headers and what is in each file: <br/>
***Edge.java*** defines the edges of graphs <br/>
***Graph.java*** defines the graph <br/>
***MapPanel.java*** uses Java Graphics to display wanted elements of the map <br/>
***MeridianMap.java*** contains takes user input, contains the main method, and implements functions for graph <br/>
***Node.java calculate*** defines the nodes of graphs <br/>
