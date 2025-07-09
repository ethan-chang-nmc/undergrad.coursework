/*
*Ethan Chang
*echang28@u.rochester.edu
*
*08/11/2024: Street Mapping
*/
import javax.swing.*;
import java.awt.*;
import java.awt.geom.Line2D;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashMap;

public class MapPanel extends JPanel 
{ 
  Graph graph; //whole graph
  List<Node> path; //shortest path
  Set<Edge> mst; //mst

  /*initializes graphs to be drawn and panel*/
  public MapPanel(Graph graph, List<Node> path, Set<Edge> mst) 
  { 
    this.graph = graph;
    this.path = path;
    this.mst = mst;
    setPreferredSize(new Dimension(800, 800)); //sets window size
  }

  /*draw graph*/
  protected void paintComponent(Graphics g) 
  { 
    super.paintComponent(g); //clears panel and prepares for rendering
    Graphics2D g2 = (Graphics2D) g; //casts the Graphics object to Graphics2D
    g2.setStroke(new BasicStroke(2)); //set stroke width for lines
    g2.setColor(Color.BLACK); //set color for map lines
    Map<String, Point> points = new HashMap<>(); //stores  screen coordinates of nodes
    double minLat = graph.nodes.values().stream().mapToDouble(n -> n.latitude).min().orElse(0); //finds  minimum latitude in graph
    double maxLat = graph.nodes.values().stream().mapToDouble(n -> n.latitude).max().orElse(1); //finds the maximum latitude in graph
    double minLon = graph.nodes.values().stream().mapToDouble(n -> n.longitude).min().orElse(0); //finds the minimum longitude in graph
    double maxLon = graph.nodes.values().stream().mapToDouble(n -> n.longitude).max().orElse(1); //findss the maximum longitude in graph
    for (Node node : graph.nodes.values())//calculate screen coordinates for each node
    {       
      int x = (int) ((node.longitude - minLon) / (maxLon - minLon) * getWidth()); //normalize longitude to fit panel width
      int y = (int) ((node.latitude - minLat) / (maxLat - minLat) * getHeight()); //normalize latitude to fit panel height
      points.put(node.id, new Point(x, y)); //stores calculated point in map
    }
    g2.setColor(Color.BLACK); //black for main graph
    for (Edge edge : graph.edges.values())//draw all edges in  graph
    {       
      Point p1 = points.get(edge.from.id); //starting point of edge
      Point p2 = points.get(edge.to.id); //ending point of edge
      g2.draw(new Line2D.Float(p1.x, p1.y, p2.x, p2.y)); //draws edge
    }
    if (mst != null) //check if MST exists
    {
      g2.setColor(Color.BLUE); //blue for mst
      for (Edge edge : mst) //draw all edges in mst
      {
        Point p1 = points.get(edge.from.id); //starting point of edge
        Point p2 = points.get(edge.to.id); //ending point of edge
        g2.draw(new Line2D.Float(p1.x, p1.y, p2.x, p2.y)); //draws edge
      }
    }
    if (path != null && path.size() > 1) //check if shortest path exists and >1
    {
      g2.setColor(Color.RED); //red for shortest path
      for (int i = 0; i < path.size() - 1; i++) //draw all edges in shortest path
      {
        Point p1 = points.get(path.get(i).id); //starting point of edge
        Point p2 = points.get(path.get(i + 1).id); //ending point of edge
        g2.draw(new Line2D.Float(p1.x, p1.y, p2.x, p2.y)); //draws edge
      }
    }
  }
}


