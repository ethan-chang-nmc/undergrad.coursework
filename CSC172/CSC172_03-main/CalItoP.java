/*
*Ethan Chang
*echang28@u.rochester.edu
*
*07/21/2024: Creating Infix Calculator
*/
public class CalItoP 
{
  /*method to convert from infix to postfix*/
  public static String infixTopostfix(String input) 
  {
    CalStack stack = new CalStack(); // makes new stack
    CalQueue queue = new CalQueue(); // makes new queue
    StringBuilder numberBuffer = new StringBuilder(); //buffer to hold a full number: i.e. 100.45
    for (int i = 0; i < input.length(); i++) // iterates through input and checks each char4.
    {
      char cinput = input.charAt(i); // sets cinput equal to input's current character
      if (Character.isDigit(cinput) || cinput == '.') 
      {
        numberBuffer.append(cinput); // collect number characters
      } 
      else if (cinput == ' ') 
      {
        if (numberBuffer.length() > 0) 
        {
          queue.enqueue(numberBuffer.toString()); // enqueue number when space is encountered
          numberBuffer.setLength(0); // clear buffer
        }
      } 
      else if (cinput == '(') 
      {
        if (numberBuffer.length() > 0) 
        {
          queue.enqueue(numberBuffer.toString()); // enqueue number before pushing '('
          numberBuffer.setLength(0); // clear buffer
        }
        stack.push(Character.toString(cinput)); // if start of parenthesis, push to stack
      } 
      else if (cinput == ')') // if end of parenthesis...
      {
        if (numberBuffer.length() > 0) 
        {
          queue.enqueue(numberBuffer.toString()); // enqueue number before processing ')'
          numberBuffer.setLength(0); // clear buffer
        }
        while (!stack.isEmpty() && !stack.peek().equals("(")) 
        {
          queue.enqueue(stack.pop()); // ...take top of stack values when stack is not empty and top value is not start of parenthesis
        }
        stack.pop(); // removes the '(' from the stack
      } 
      else if (isOperator(cinput)) // if is an operator
      {
        if (numberBuffer.length() > 0) 
        {
          queue.enqueue(numberBuffer.toString()); // enqueue number before pushing operator
          numberBuffer.setLength(0); // clear buffer
        }
        while (!stack.isEmpty() && precedence(stack.peek().charAt(0)) >= precedence(cinput)) 
        {
          queue.enqueue(stack.pop()); // adds top of stack to queue as long as stack is not empty and the precedence of stack value is greater than current
        }
        stack.push(Character.toString(cinput)); // add current operator to stack
      }
    }
    if (numberBuffer.length() > 0) 
    {
      queue.enqueue(numberBuffer.toString()); // add remaining number to queue
    }
    while (!stack.isEmpty()) 
    {
      queue.enqueue(stack.pop()); // add remaining things from stack to queue
    }
    return queueTostring(queue); // returns string value of postfix 
  }

  // method to check to see if char is one of 5 operators
  private static boolean isOperator(char token) 
  {
    return token == '+' || token == '-' || token == '*' || token == '/' || token == '^'; // if char is equal to any of the 5 characters, return true
  }

  // function to return precedence of operators
  private static int precedence(char operator) 
  {
    switch (operator) //cases
    {
      case '+': case '-': return 1; // lowest priority for addition and subtraction
      case '*': case '/': return 2; // middle priority for multiplication and division
      case '^': return 3; // highest priority for exponentiation
      default: return -1; // value for invalid operator
    }
  }

  /*function to convert queue to string (postfix expression)*/
  private static String queueTostring(CalQueue queue) 
  {
    StringBuilder result = new StringBuilder(); // hold postfix values
    while (!queue.isEmpty()) 
    {
      result.append(queue.dequeue()).append(" "); // add values while they exist in queue to string
    }
    return result.toString().trim(); // return string values without extra spaces on sides
  }
}

