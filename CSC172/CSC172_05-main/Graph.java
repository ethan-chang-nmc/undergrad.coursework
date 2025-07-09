/*
*Ethan Chang
*echang28@u.rochester.edu
*
*08/11/2024: Street Mapping
*/
import java.util.*;

public class Graph 
{
  Map<String, Node> nodes = new HashMap<>(); //store nodes by their id
  Map<String, Edge> edges = new HashMap<>(); //store edges by their id
  Map<Node, List<Edge>> adjacencyList = new HashMap<>(); //adjacency list for graph

  /*adds node to the graph*/
  public void addNode(Node node) 
  {
    nodes.put(node.id, node);
    adjacencyList.putIfAbsent(node, new ArrayList<>());
  }

  /*adds edge to the graph*/
  public void addEdge(Edge edge) 
  { 
    edges.put(edge.id, edge);
    adjacencyList.get(edge.from).add(edge);
    adjacencyList.get(edge.to).add(edge);
  }

  /*Dijkstra's algorithm*/
  public List<Node> dijkstra(String startId, String endId) 
  { 
    Node start = nodes.get(startId); //gets start node id
    Node end = nodes.get(endId); //gets end node id
    Map<Node, Node> previous = new HashMap<>(); //map tracking the previous node in the shortest path
    Map<Node, Double> distances = new HashMap<>(); //map storing the min distances from the start node
    PriorityQueue<Node> queue = new PriorityQueue<>(Comparator.comparing(distances::get)); //priority queue based on minimum distance
    for (Node node : nodes.values()) 
    {
      distances.put(node, Double.POSITIVE_INFINITY); //initial distances set to infinity
      previous.put(node, null); //previous nodes set to null
    }
    distances.put(start, 0.0); //sets the distance to the start node as 0
    queue.add(start); //adds the start node to the priority queue
    while (!queue.isEmpty()) //loops through priority
    {
      Node current = queue.poll(); //gest  node with the smallest distance
      if (current.equals(end)) break; //stops at end node
      for (Edge edge : adjacencyList.get(current)) //iterates through all edges connected to current node
      {
        Node neighbor = edge.to.equals(current) ? edge.from : edge.to; //get neighbor node
        double alt = distances.get(current) + edge.weight; //calculate second distance to neighbor
        if (alt < distances.get(neighbor)) //checks if second is shorter
        {
          distances.put(neighbor, alt); //updats shortest distance
          previous.put(neighbor, current); //sets  current node as the previous node for neighbor
          queue.add(neighbor); //adds neighbor to the priority queue
        }
      }
    }
    List<Node> path = new ArrayList<>(); //stores the shortest path
    for (Node at = end; at != null; at = previous.get(at)) //backtrack end node for path
    {
      path.add(at); //add current node to the path
    }
    Collections.reverse(path); //revers the path to get start to end
    return path; //return the shortest path nodes
  }

  /*method to find mst*/
  public Set<Edge> minimumSpanningTree() 
  { 
    Set<Edge> mst = new HashSet<>(); //stores edges
    PriorityQueue<Edge> edgesQueue = new PriorityQueue<>(Comparator.comparing(edge -> edge.weight)); //priority queue for edge based on weight
    Set<Node> visited = new HashSet<>(); //tracks visited node
    Node startNode = nodes.values().iterator().next(); //selects a starting node
    visited.add(startNode); //mark starting node visited
    edgesQueue.addAll(adjacencyList.get(startNode)); //adds all edges connected to the starting node to the queue
    while (!edgesQueue.isEmpty() && mst.size() < nodes.size() - 1) //loop till mst complete
    {
      Edge edge = edgesQueue.poll(); //gets edge with smallest weight
      Node node = visited.contains(edge.from) ? edge.to : edge.from; //determines the next node to visit
      if (!visited.contains(node)) //checks if node already visited
      { 
        visited.add(node); //marks node visited
        mst.add(edge); //add edge to the mst
        edgesQueue.addAll(adjacencyList.get(node)); //add all edges connected to newly visited node to queue
      }
    }
    return mst; //returns edges in the mst
  }
}
