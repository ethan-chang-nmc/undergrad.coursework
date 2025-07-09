/*
*Ethan Chang
*echang28@u.rochester.edu
*
*08/11/2024: Street Mapping
*/
public class Edge 
{
  String id; //id of edge
  Node from, to; //start, end nodes of  edge
  double weight; //distance between nodes

  /*initiallizes edge*/
  public Edge(String id, Node from, Node to) 
  {
    this.id = id; //assign edge id
    this.from = from; //assign start node
    this.to = to; //assign end node
    this.weight = calculateDistance(from, to); //calculates and assigns weight of edge
  }

  /*calculates  distance between two nodes using Haversine formula*/
  private double calculateDistance(Node a, Node b) 
  { 
    double lat1 = Math.toRadians(a.latitude); //latitude to radians of node a
    double lon1 = Math.toRadians(a.longitude); //longitude to radians of node a
    double lat2 = Math.toRadians(b.latitude); //latitude to radians of node b
    double lon2 = Math.toRadians(b.longitude); //longitude to radians of node b
    double dlon = lon2 - lon1; //difference in longitudes
    double dlat = lat2 - lat1; //difference in latitudes
    double aHarv = Math.pow(Math.sin(dlat / 2), 2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(dlon / 2), 2);//Haversine formula
    double cHarv = 2 * Math.asin(Math.sqrt(aHarv)); //Haversine formula
    double R = 3956; //radius of the Earth in miles
    return R * cHarv; //returns distance between nodes
  }
}
