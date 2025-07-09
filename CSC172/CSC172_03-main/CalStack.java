/*
*Ethan Chang
*echang28@u.rochester.edu
*
*07/21/2024: Creating Infix Calculator
*/
class CalStack 
{
  CalLinkedList list = new CalLinkedList(); //initialize new linked list
  /*push function to add item onto stack*/
  public void push(String data) 
  {
    list.insert(data); //insert into stack
  }

  /*pop function to remove item from top of stack*/
  public String pop() 
  {
    if (list.isEmpty()) 
    {
      return null; //checks for case where list is empty
    }
    // Implement a method to remove the last added item (not shown here for brevity)
    return list.delFirst();
  }

  /*method to check if stack is empty*/
  public boolean isEmpty() 
  {
    return list.isEmpty(); //checks if stack is empty
  }

  /*method to check first element of stack*/
  public String peek() 
  {
    return list.peekFirst(); //gives value of top of stack
  }
}
