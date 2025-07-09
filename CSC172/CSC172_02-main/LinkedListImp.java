/*
*Ethan Chang
*echang28@u.rochester.edu
*
*Partner: Darron King
*
*07/14/2024: Creating Linked List and Functions
*/

/*Implementation of methods in interface MyLinkedLIst*/
public class LinkedListImp implements MyLinkedList 
{
  MyNode head = null; //creates and sets head node to null

  /*Creates a new node with x as data and adds it to the front of the linked list: Runtime O(1) since operation # stays the same no matter size n*/
  public void insert(Object x)
  {
    if (lookup(x) == true) //checks to see if value already exists inside the linked list
    {
      return; //if value is in list, do not insert the value into the list
    }
    MyNode newNode = new MyNode(); //makes new node
    newNode.data = x; //set that data in new node to x
    newNode.next = head; //have next in new node point to next element in linked list (null if end)
    head = newNode; //set head to first element in the linked list
  }

  /*Iterates through linked list and prints each element: Runtime O(n) since it has to go through list of n elements*/
  public void  printList()
  {
    MyNode printNode = head; //temporary holder for current node to be printed
    while (printNode != null) //iterates through linked list until end
    {
      System.out.println(printNode.data); //print the data of current node
      printNode = printNode.next; //have the current node be the next node in linked list
    }
  }

  /*Implements a lookup function to find if a value is in the linked list*/
  public boolean lookup(Object x)
  {
    MyNode lookNode = head; //temporary holder for current node to be looked at
    while (lookNode != null) //iterates through linked list
    {
      if (lookNode.data.equals(x)) //if current node equal x, return true
      {
        return true;
      }
      lookNode = lookNode.next; //move to next node in list
    }
    return false; //return false if item was not found in array
  }

  /*Implements a delete function that deletes the value if it is in the linked list*/
  public void delete(Object x)
  {
    if (lookup(x) == false) //checks to see if value is inside the linked list
    {
      return; //if value is not in list, returns (does nothing) 
    }
    MyNode delNode = head; //temporary holder for current node
    MyNode prevNode = null; // To keep track of the previous node

    // Iterate through the linked list
    while (delNode != null) 
    {
      if (delNode.data.equals(x)) // If the current node equals x, remove this node
      {
        if (prevNode == null) // First node case
        {
          head = delNode.next; //Move the head to the next node
        } 
        else 
        {
          prevNode.next = delNode.next; //Link previous node with next node
        }
        return; // Node deleted, exit the method
      }
    prevNode = delNode; //move to next node
    delNode = delNode.next;
    }
  }
}
