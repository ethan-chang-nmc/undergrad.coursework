/*
*Ethan Chang
*echang28@u.rochester.edu
*
*Partner: Darron King
*
*07/28/2024: Creating Binary Search Trees
*/
public class mainBST
{
  public static void main(String[] args) 
  {
    MyBST<Integer> bst = new ImplementBST<>(); //creating new bst for testing
    bst.insert(5);
    bst.insert(3);
    bst.insert(7);
    bst.insert(2);
    bst.insert(4);
    bst.insert(6);
    bst.insert(8);

   System.out.print("InOrder before deletion: ");
    bst.printInOrder();
    System.out.println();
    //expected Output: 2 3 4 5 6 7 8 

    System.out.print("PreOrder before deletion: ");
    bst.printPreOrder();
    System.out.println();
    //expected Output: 5 3 2 4 7 6 8 

    System.out.print("PostOrder before deletion: ");
    bst.printPostOrder();
    System.out.println();
    //expected Output: 2 4 3 6 8 7 5 

    bst.delete(3); //Node with two children
    bst.delete(7); //Node with one child
    bst.delete(2); //Leaf node

    System.out.print("InOrder after deletions: ");
    bst.printInOrder();
    System.out.println();
    //expected Output: 4 5 6 8 

    System.out.print("PreOrder after deletions: ");
    bst.printPreOrder();
    System.out.println();
    //expected Output: 5 4 8 6 

    System.out.print("PostOrder after deletions: ");
    bst.printPostOrder();
    System.out.println();
    //expected Output: 4 6 8 5 
    
    System.out.println("Lookup 4: " + bst.lookup(4)); //expected: true 
    System.out.println("Lookup 9: " + bst.lookup(9)); //expected: false
    }
}
