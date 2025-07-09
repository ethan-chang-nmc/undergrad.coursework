/*
*Ethan Chang
*echang28@u.rochester.edu
*
*07/21/2024: Creating Infix Calculator
*/
class CalQueue 
{
  CalLinkedList list = new CalLinkedList(); //initialize new linked list
  /*function to add new data to queue*/
  public void enqueue(String data) 
  {
    list.insert(data);//adds new data to queue
  }

  /*function that removes last item in linked list queue*/
  public String dequeue() 
  {
    return list.delLast(); //removes last data in linked list
  }

  /*checks to see if queue is empty*/
  public boolean isEmpty() 
  {
    return list.isEmpty();//chekcs to see if queue is empty
  }
}
