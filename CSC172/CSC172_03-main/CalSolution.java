/*
*Ethan Chang
*echang28@u.rochester.edu
*
*07/21/2024: Creating Infix Calculator
*/
public class CalSolution 
{
  /*method to calculate input equation*/
  public String calculate(String input) 
  {
    String postfixval = CalItoP.infixTopostfix(input); //calls on function to change from infix to postfix
    double finval = CalPostfix.calculatePostfix(postfixval); //calls on function to evaluate postfix equation
    return Double.toString(finval); //returns value calculated
  }
}
