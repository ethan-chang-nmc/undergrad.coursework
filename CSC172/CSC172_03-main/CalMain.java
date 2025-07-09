/*
*Ethan Chang
*echang28@u.rochester.edu
*
*07/21/2024: Creating Infix Calculator
*/
import java.util.Scanner;

public class CalMain 
{
  /*main user interface*/
  public static void main(String[] args) 
  {
    CalSolution calc = new CalSolution(); //new CalSolution
    Scanner scan = new Scanner(System.in); //Defines scanner to read user input
    try
    {
      System.out.println("Please enter an infix equation to evaluate:"); //prompts user for input
      String userinp = scan.nextLine(); //reads user input
      String result = calc.calculate(userinp); //calculates value from user input
      System.out.println("Calculated value: " + result); //prints out calculated value
    }
    finally 
    {
      scan.close(); //close scan when finished
    }
  }
}
