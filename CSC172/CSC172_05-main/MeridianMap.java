/*
*Ethan Chang
*echang28@u.rochester.edu
*
*08/11/2024: Street Mapping
*/
import java.io.*;
import java.util.*;
import javax.swing.*;

public class MeridianMap 
{ 
  public static void main(String[] args) 
  { 
    if (args.length < 1) //checks if argument is valid
    { 
      System.out.println("Usage: java MeridianMap map.txt [-show] [-directions startIntersection endIntersection] [-meridianmap]"); //usage instructions if invalid
      return; //exits program
    }
    String filename = args[0]; //map file name
    boolean showMap = false; //flag if map should be displayed
    String startIntersection = null, endIntersection = null; //start and end intersections for shortest path
    boolean showMST = false; //flag if mst should be sdisplayed
    for (int i = 1; i < args.length; i++) //process additional arguments
    {
      switch (args[i]) 
      { 
        case "-show": //show the map
          showMap = true; //display map
          break;
        case "-directions": //find and display shortest path
          if (i + 2 < args.length) //checks for start and end instersections
          {
            startIntersection = args[i + 1]; //set start intersection
            endIntersection = args[i + 2]; //set end intersection
            i += 2; //skips next two arguments
          }
          break;
        case "-meridianmap": //display mst
          showMST = true; //display mst
          break;
      }
    }
    Graph graph = new Graph();
    try (BufferedReader br = new BufferedReader(new FileReader(filename))) //tries to read file
    { 
      String line; 
      while ((line = br.readLine()) != null) //real line by line
      {
        String[] parts = line.split("\\s+"); //splits each line into parts
        if (parts[0].equals("i")) //check if line defines node
        {
          Node node = new Node(parts[1], Double.parseDouble(parts[2]), Double.parseDouble(parts[3])); //creates a new node
          graph.addNode(node); //adds  node to graph
        } 
        else if (parts[0].equals("r")) //check if line defines edge
        {
          Node from = graph.nodes.get(parts[2]); //get start node for edge
          Node to = graph.nodes.get(parts[3]); //get end node for edge
          Edge edge = new Edge(parts[1], from, to); //creates new edge
          graph.addEdge(edge); //add edge to graph
        }
      }
    } 
    catch (IOException e) //catch exceptions when reading file
    {
      System.out.println("Error reading file: " + e.getMessage()); //error message if file reading fails
      return; //exit program
    }
    List<Node> path = null; 
    if (startIntersection != null && endIntersection != null) //shortest path requested from user
    { 
      path = graph.dijkstra(startIntersection, endIntersection); //finds the shortest path
      double totalDistance = path.stream().mapToDouble(node -> graph.edges.values().stream()
        .filter(edge -> edge.from.equals(node) || edge.to.equals(node)) 
        .mapToDouble(edge -> edge.weight) 
        .min().orElse(0)) 
        .sum(); //calculates the total distance of the shortest path
      System.out.println("Shortest path from " + startIntersection + " to " + endIntersection + ":"); //prints the shortest path
      path.forEach(node -> System.out.print(node.id + " ")); //prints each node in  path
      System.out.println("\nTotal Distance: " + totalDistance + " miles"); //prints  total distance of the path
    }
    Set<Edge> mst = null; 
    if (showMST) //msst requested from user
    { 
      mst = graph.minimumSpanningTree(); //calculates mst
      System.out.println("Minimum Weight Spanning Tree edges:"); //prints edges in mst
      mst.forEach(edge -> System.out.println(edge.id + ": " + edge.from.id + " - " + edge.to.id)); //prints edge's details
    }
    if (showMap) //map display requested from user
    { 
      JFrame frame = new JFrame("Meridian Map"); //JFrame to display the map
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //default close by exit
      frame.add(new MapPanel(graph, path, mst)); //adds mappanel to frame
      frame.pack(); //sizes the frame
      frame.setVisible(true); //make frame visible
    }
  }
}

