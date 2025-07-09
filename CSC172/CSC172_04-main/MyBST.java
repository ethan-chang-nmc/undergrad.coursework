/*
*Ethan Chang
*echang28@u.rochester.edu
*
*Partner: Darron King
*
*07/28/2024: Creating Binary Search Trees
*/
public interface MyBST <T extends Comparable<T>>
{
  public void insert(T x);
  public void delete(T x);
  public boolean lookup(T x);
  public void printPreOrder();
  public void printInOrder();
  public void printPostOrder();
} 
