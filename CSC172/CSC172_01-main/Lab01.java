/*
*Ethan Chang
*echang28@u.rochester.edu
*
*Partner: Darron King
*
*07/07/2024: Implementing a print array and get maximum function
*/
import java.util.function.Function;

public class Lab01 
{
    public static void main(String[] args) 
    {
        /*problems 1-3*/
        Integer [] intArry = {1, 2, 3, 4, 5 };
        Double [] doubArry = {1.1, 2.2, 3.3, 4.4};
        Character [] charArry = {'H','E','L', 'L', 'O' };
        String [] strArry = {"once", "upon", "a", "time" };
        printArray(intArry);
        printArray(doubArry);
        printArray(charArry);
        printArray(strArry);
        
        /*problems 4-5*/
        System.out.println("max Integer is: " + getMax(intArry));
        System.out.println("max Double is: " + getMax(doubArry));
        System.out.println("max Character is: " + getMax(charArry));
        System.out.println("max String is: " + getMax(strArry)) ;

        /*creating a function for max character*/
        Function<Character[], Character> findMax = (Character[] inpArray) -> //map char array to char
        {
            Character max = inpArray[0]; //set max char to first char
            for (int i = 1; i < inpArray.length; i++) //iterrates through char array and replaces max with larger char
            {
                if (inpArray[i].compareTo(max) > 0) 
                {
                    max = inpArray[i];
                }
            }
            return max;
        };
        System.out.println("max Character is: " + findMax.apply(charArry));
    }

    /*
    *Implementation of the getMax function, which iterates through an input array and returns the max value
    */
    /*SECOND IMPLEMENTATION OF getMax WITH GENERICS */
    public static <T extends Comparable<T>> T getMax(T[] anArray)
    {
        T maxval = anArray[0]; //getting the first value in the array
        for (int i = 1; i < anArray.length; i++) //iterrating through the array to the end
        {
            if (anArray[i].compareTo(maxval)>0) //comparing two values and storing the greater value into maxval
            {
                maxval = anArray[i];
            }
        }
        return maxval;
    }

    /*FIRST IMPLEMENTATION OF getMax WITHOUT GENERICS
    *Errors:
    *Comparable is a raw type. References to generic type Comparable<T> should be parameterized
    *Type safety: The method compareTo(Object) belongs to the raw type Comparable. References to generic type Comparable<T> should be parameterized
    
    public static Comparable getMax(Comparable[] anArray)
    {
        Comparable maxval = anArray[0]; //getting the first value in the array
        for (int i = 1; i < anArray.length; i++) //iterrating through the array to the end
        {
            if (anArray[i].compareTo(maxval)>0) //comparing two values and storing the greater value into maxval
            {
                maxval = anArray[i];
            }
        }
        return maxval;
    }
    */

    /*
    *Implementation of the print array function, which iterates through an input array and prints each element
    */
    /*THIRD IMPLEMENTATION OF printArray USING GENERICS*/
    public static <T> void printArray(T[] array) 
    {
        for (T element : array) //go through each element in the array
        {
            System.out.print(element + " "); //print out that element, seperated by spaces
        }
        System.out.println(); //new line for next time it is called
    }
    
    /*SECOND IMPLEMENTATION OF printArray USING METHOD OVERLOADING
    
    public static void printArray(Integer[] array) 
    {
        for (int element : array) //go through each element in the array
        {
            System.out.print(element + " "); //print out that element, seperated by spaces
        }
        System.out.println(); //new line for next time it is called
    }
    public static void printArray(Double[] array) 
    {
        for (double element : array) //go through each element in the array
        {
            System.out.print(element + " "); //print out that element, seperated by spaces
        }
        System.out.println(); //new line for next time it is called
    }
    public static void printArray(Character[] array) 
    {
        for (char element : array) //go through each element in the array
        {
            System.out.print(element + " "); //print out that element, seperated by spaces
        }
        System.out.println(); //new line for next time it is called
    }
    public static void printArray(String[] array) 
    {
        for (String element : array) //go through each element in the array
        {
            System.out.print(element + " "); //print out that element, seperated by spaces
        }
        System.out.println(); //new line for next time it is called
    }
    */
    
    /*FIRST IMPLEMENTATION USING OBJECT

    public static void printArray(Object[] array)
    {
        for (Object element : array) //go through each element in the array
        {
            System.out.print(element + " "); //print out that element, seperated by spaces
        }
        System.out.println(); //new line
    }
    */
}
