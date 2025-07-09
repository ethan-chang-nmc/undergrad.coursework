/*
*Ethan Chang
*echang28@u.rochester.edu
*
*Partner: Darron King
*
*07/28/2024: Creating Binary Search Trees
*/
public class ImplementBST<T extends Comparable<T>> implements MyBST<T>
{
  public MyTreeNode<T> root = null; //create root node

  /*insert method calling on recursive insert*/
  public void insert(T x) 
  {
    if (!lookup(x)) //only inserts if it does not already exist in BST
    {
      root = insertRec(root, x, null);
    }
  }

/*recursive insert method*/
private MyTreeNode<T> insertRec(MyTreeNode<T> node, T x, MyTreeNode<T> parent) 
{
  if (node == null) //empty case
  {
    MyTreeNode<T> newNode = new MyTreeNode<>(); //create new node
    newNode.data = x; //set node data equal to x
    newNode.parent = parent; //set node's parent
    return newNode;
  }
  if (x.compareTo(node.data) < 0) 
  {
    node.leftchild = insertRec(node.leftchild, x, node); //recursively call function for left side and current node as parent
  } 
  else if (x.compareTo(node.data) > 0) 
  {
    node.rightchild = insertRec(node.rightchild, x, node); //recursively call function for right side and current node as parent
  }
  return node; //if equal to the current node, do nothing to prevent duplicates
}

  /*PreOrder method calling on recursive PreOrder*/
  public void printPreOrder() 
  {
    root.printPreOrderRec(root);
  }

  /*InOrder method calling on recursive InOrder*/
  public void printInOrder() 
  {
    root.printInOrderRec(root);
  }

  /*PostOrder method calling on recursive PostOrder*/
  public void printPostOrder() 
  {
    root.printPostOrderRec(root);
  }

  /*lookup method calling on recursive lookup*/
  public boolean lookup(T x) 
  {
    return lookupRec(root, x);
  }

  /*recursive lookup method*/
  private boolean lookupRec(MyTreeNode<T> node, T x) 
  {
    if (node == null)
    {
      return false; //return false if null
    }
    if (x.compareTo(node.data) == 0) 
    {
      return true; //returns true if node is found
    } 
    else if (x.compareTo(node.data) < 0) 
    {
      return lookupRec(node.leftchild, x); //continue traversing left if less than current node
    } 
    else 
    {
      return lookupRec(node.rightchild, x); //continue traversing right if greater than current node
    }
  }

  /*delete method calling on recursive delete*/
  public void delete(T x) 
  {
    if (lookup(x)) //only calls delete if x is in BST
    {
      root = root.deleteRec(root, x);
    }
  }
}
