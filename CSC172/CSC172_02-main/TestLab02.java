/*
*Ethan Chang
*echang28@u.rochester.edu
*
*Partner: Darron King
*
*07/14/2024: Creating Linked List and Functions
*/

/*testing
 *Expected Output:
 *Third
 *First
*/
public class TestLab02 
{
  public static void main(String[] args) 
  {
    LinkedListImp testList = new LinkedListImp(); //create linked list
    //Insert values into the linked list then print
    testList.insert("First");
    testList.insert("Second");
    testList.insert("Third");
    testList.insert("Second"); //check to see insert ignores if x is already in list
    testList.delete("Four"); //check to see delete ignores if x is not in list
    testList.delete("Second");
    testList.printList();
  }
}
