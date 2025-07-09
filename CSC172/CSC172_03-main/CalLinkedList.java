/*
*Ethan Chang
*echang28@u.rochester.edu
*
*07/21/2024: Creating Infix Calculator
*Code adapted from Lab 2
*/
class CalLinkedList 
{
  CalNode head = null; //creates and sets head node to null

  /*Creates a new node with x as data and adds it to the front of the linked list*/
  public void insert(String x)
  {
    CalNode newNode = new CalNode(); //makes new node
    newNode.data = x; //set that data in new node to x
    newNode.next = head; //have next in new node point to next element in linked list (null if end)
    head = newNode; //set head to first element in the linked list
  }

  /*checks to see if list is empty*/
  public boolean isEmpty() 
  {
    return head == null; //when list is empty, head is null and returns true
  }

  /*looks at first element of list and returns the value*/
  public String peekFirst() 
  {
    if (head == null) //checks for case where list is empty
    {
      return null; //returns null if true
    }
    return head.data; //otherwise, return firsts element
  }

  /*removes last element in list*/
  public String delLast() 
  {
    if (head == null) //checks for case where list is empty
    {
      return null; //returns null if true
    }
    if (head.next == null) //checks for cases where there is only one element in list
    {
      String data = head.data; //set data equal to only element in list
      head = null; //move head pointer to null
      return data; //return the element
    }
    CalNode prev = null; //set prev node equal to null
    CalNode current = head; //set current node equal to head
    while (current.next != null) //while loop to iterate through linked list until current node is last node
    {
      prev = current; //move previous node to where current node is
      current = current.next; //shift current node one spot forward
    }
    String data = current.data; //sets data equal to value of last node
    prev.next = null; //removes last node
    return data; //returns last element in list
  }
  
  /*removes first element in list*/
  public String delFirst() 
  {
    if (head == null) 
    {
      return null; //checks for case where list is empty
    }
    String data = head.data; //set data = first element in list
    head = head.next; //shifts head pointer to next element in list
    return data; //returns first element (before removal) in list
  }
}
