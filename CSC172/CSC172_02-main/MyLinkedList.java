/*
*Ethan Chang
*echang28@u.rochester.edu
*
*Partner: Darron King
*
*07/14/2024: Creating Linked List and Functions
*/

/*Linked List Interface*/
public interface MyLinkedList 
{
  public void insert(Object x);
  /*
  public void insertFirst(Object x);
  public void insertLast(Object x);
  */
  public void delete(Object x);
  public boolean lookup(Object x);
  public void printList();
} 
