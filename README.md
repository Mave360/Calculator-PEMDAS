# PEMDAS Calculator
#### Video Demo:  <https://www.youtube.com/watch?v=a3tPdwxQz-s>
#### Description: A Basic PEMDAS Calculator that respects the order of precedence
    
This is the README file of my final project for my CS50P introduction to programming with Python. Within this file, I'm going to explain what my project is, and details about the software I created using Python. I would like to introduce, specifically the different steps that I had to go through before even starting to code a PEMDAS calculator. 

First, I would like to acknowledge that I had no idea how to start coding my project. So I had to do some research on what were the steps to make a PEMDAS calculator. I found a video on YouTube from an experimented C# developer explaining the process of how to make the calculator. It's divided into different steps, which are the following:

### 1. Validating the user's input
### 2. Storing the user's input into tokens
### 3. Stating the order of precedence of the operators according to the PEMDAS rules
### 4. Convert the order of the tokens from the user from infix to postfix notation
### 5. Apply the mathematical logic according to the postfix notation to solve the expression
### 6. Extra step: Add a visual GUI to the calculator


### 1. Validating the user's input
Let's start with the first step, which would be validating the user's input. This step is quite simple, but a little bit challenging. It is one of the multiple steps in which we are gonna need the regular expressions or regex library to simplify our code as much as we can. Regular expressions are very useful when it comes to validating user input, it doesn't matter what kind of area you want to use it with, it is the language used to validate emails for example. Therefore, I thought it would be a brilliant idea to use the regex library to validate the user's input for my calculator's entry. If the user submits an input that's not valid, a ValueError will be triggered and raised, returning a 
"Invalid input" message that the user will be able to see. This prevents the user from providing inputs that can't be evaluated by the calculator, like "cat" or "Cat + Dog". If the user's input is valid, the code keeps going with the rest of the steps.

### 2. Storing user's input into tokens

The following step would be storing the user's input into tokens. To store the user's input into tokens within Python, we would have to convert the user's input from a string into a list of tokens, which we are going to use later to perform the mathematical evaluations. When converting the user's input into tokens you might think that the "split" method would work and be enough to convert the string into a list of tokens. This is partially true, however, the split method has some inconveniences, for example, if we use decimal numbers, we would need the decimal number to be stored as a single token (or list character). However, it is a little bit complicated to make this work by simply using the built-in functions, therefore, again I thought about using the regex library to tokenize the user's input effectively.
That way, we can store every type of number, operator, and even negative numbers as a single token and save them into a list of tokens.

### 3. Stating the order of precedence of the operators according to the PEMDAS rules

This is a step that you should perform before even starting to code your calculator, even if you just have it as a comment within your code. In Python, we will use a dictionary to store the keys and values of the operators and their precedence. I named the dictionary PEMDAS and the keys are the string representation of the operator, and the value of each key is a number that is higher or lower depending on the order of precedence. Here is the dictionary:

PEMDAS = {'+': 4, '-': 4, '*': 5, '/': 5, '%': 9, '√': 7, "^": 10, '(': 1, ')': 1, "[": 2, "]": 2, "{": 3, "}": 3 }

### 4. Convert the order of the tokens from the user from infix to postfix notation

Alright, here is the step of building the calculator that was the most difficult for me. This step simply consists of converting the user's input from the regular notation that we use in mathematical expressions, called infix notation, into RPN(Reverse Polish Notation), or Postfix notation. 

But why should we use RPN or Postfix notation instead of the infix notation? Before diving into explaining what is the postfix notation, we need to understand first, why is it used. Here are several reasons why using postfix notation can be beneficial:

1. Eliminates the Need for Parentheses
Postfix notation inherently captures the order of operations without requiring parentheses. This simplifies both the input and the evaluation process. In infix notation, parentheses are used to explicitly specify the order of operations, which can make expressions more complex.

2. Simplifies Expression Evaluation:

With postfix notation, you can evaluate expressions directly using a stack-based algorithm, which is very efficient and straightforward. You push operands onto a stack and pop and apply operators when they are encountered. This eliminates the need for complex recursive or nested parsing algorithms that are often required when evaluating infix expressions.

3. No Need for Operator Precedence Rules:
In infix notation, you need to follow operator precedence rules (e.g., multiplication before addition). Converting to postfix notation naturally preserves the order of operations, so you don't need to worry about precedence rules when evaluating the expression.

4. Avoids Ambiguities:

In infix notation, expressions like "2 + 3 * 4" require an understanding of operator precedence to know that multiplication should be done before addition. Postfix notation makes the order of operations explicit, so there's no ambiguity. "2 3 4 * +" clearly indicates that multiplication is done before addition.

5. Easily Extensible for New Operators:

Adding new operators to your calculator becomes more straightforward with postfix notation. You can simply define the operator's precedence and associativity and update the evaluation algorithm accordingly. In infix notation, you would need to modify the parsing logic to account for new operators.

6. Reduces Memory Usage:

Postfix notation often requires less memory because you don't need to store operator precedence or maintain a complex parse tree. This can be particularly important in resource-constrained environments.

7. Supports Function Evaluation:

Postfix notation naturally supports the evaluation of mathematical functions (e.g., sin, cos, log) as well as user-defined functions. Functions can be treated as operators in the postfix expression, making it easier to integrate them into your calculator.

To summarize, converting infix notation to postfix notation simplifies expression evaluation, eliminates the need for explicit parentheses, and ensures adherence to the PEMDAS/BODMAS order of operations, making it a practical choice for implementing a calculator software that handles complex mathematical expressions.


Postfix notation is a mathematical notation in which the operators follow their operands. In other words, instead of writing expressions with operators in between operands (infix notation), postfix notation places operators after their operands. This notation was popularized by the computer scientist Charles Hamblin and is often used in computing, calculators, and programming languages for efficient expression evaluation.

Here's how postfix notation works:

Operators Follow Operands: In postfix notation, you write an expression in such a way that operators come after their corresponding operands. There are no parentheses needed to specify the order of operations because it is unambiguous. Each operator operates on the nearest operands to its left.

No Operator Precedence Rules: Postfix notation eliminates the need for operator precedence rules (e.g., PEMDAS/BODMAS) because the order of operations is determined solely by the arrangement of the expression. This simplifies parsing and evaluation.

Example: Let's take an example expression in infix notation: "3 + 4 * 2." In postfix notation, this expression would be written as "3 4 2 * +."

"3" and "4" are operands, so they are written first.
"*" is an operator, and it follows its two operands, "4" and "2."
"+" is also an operator, and it follows the result of the multiplication, which is "8" (4 * 2).
So, in postfix notation, you evaluate the expression from left to right, and the result is "3 + 8," which equals 11.

So, first of all, to convert a notation from infix notation to postfix notation we would have to use an algorithm called the Shunting Yard algorithm. 

Here's an overview of how the Shunting Yard algorithm works:

-Initialize two data structures: a stack for operators and an output queue (or output list) for the postfix notation.
-Iterate through each token in the input infix expression from left to right.
-If the token is an operand (a number or variable), add it to the output queue.
-If the token is an operator, there are a few possibilities:
-While the stack is not empty and the operator at the top of the stack has greater precedence or the same precedence (in the case of left-associative operators) than the current operator, pop operators from the stack and add them to the output queue.
-Push the current operator onto the stack.
-If the token is an open parenthesis '(', push it onto the stack.
-If the token is a closing parenthesis ')', pop operators from the stack and add them to the output queue until an open parenthesis is encountered. Pop and discard the open parenthesis.
-After processing all tokens in the input expression, pop any remaining operators from the stack and add them to the output queue.
-The output queue now contains the expression in postfix notation, and you can evaluate it using a stack-based algorithm.
Here's an example to illustrate the Shunting Yard algorithm:

Input infix expression: 3 + 4 * (2 - 1)

-Start with an empty stack and an empty output queue.
-Process each token:
-Token: 3 (operand) -> Add to output queue.
-Token: + (operator) -> Push onto stack.
-Token: 4 (operand) -> Add to output queue.
-Token: * (operator) -> Push onto stack.
-Token: ( (open parenthesis) -> Push onto the stack.
-Token: 2 (operand) -> Add to output queue.
-Token: - (operator) -> Push onto stack.
-Token: 1 (operand) -> Add to output queue.
-Token: ) (close parenthesis) -> Pop operators from stack and add to output until '(' is encountered. Discard '('.
-Pop any remaining operators from the stack and add them to the output queue (in this case, just '+' is left on the stack).
--Output queue: 3 4 2 1 - * +
--The postfix expression "3 4 2 1 - * +" can now be evaluated using a stack, resulting in the value 7.

The Shunting Yard algorithm is a powerful tool for parsing and evaluating expressions and is a fundamental component of many computer programs that deal with mathematical calculations.

After explaining how the Shunting Yard Algorithm works according to what I researched. I had to do the hardest part, which would be implementing it into my code. So, I created a function that would organize the tokenized list from infix notation into postfix notation. The function is called "Shunting Yard" which follows the instructions to apply the shunting yard algorithm that I explained before. The function re-organizes the tokenized version from infix to postfix notation, removing parentheses and brackets.

### 5. Apply the mathematical logic according to the postfix notation to solve the expression

Evaluation of a mathematical expression in postfix notation is done using a stack-based algorithm. This algorithm is designed to process the expression from left to right while efficiently handling operands and operators. Here are the steps to evaluate a postfix expression:

1. Initialize an Empty Stack: Create an empty stack data structure. This stack will be used to store operands as you process the expression.

2. Scan the Expression from Left to Right: Start scanning the postfix expression one token at a time, whether it's an operand or an operator.

3. For Each Token:
    -If the token is an operand (a number or variable), push it onto the stack.
    -If the token is an operator, pop the top two operands from the stack.
        - The first popped operand becomes the right operand.
        - The second popped operand becomes the left operand.
        - Apply the operator to the two operands.
        - Push the result back onto the stack.

4. Repeat Step 3:** Continue scanning the expression and applying operators as long as there are tokens left.

5. Result: When you have processed all the tokens, the stack should contain a single value, which is the final result of the expression.

6. Return the Result: Pop the result from the stack, and that is your answer.

Here's an example to illustrate the evaluation of a postfix expression: "3 4 2 * +"

1. Initialize an empty stack (which would be a Python empty list): [] 

2. Start scanning the expression from left to right:
    - Token: 3 (operand) -> Push onto the stack: [3]
    - Token: 4 (operand) -> Push onto the stack: [3, 4]
    - Token: 2 (operand) -> Push onto the stack: [3, 4, 2]
    - Token: * (operator) -> Pop 2 and 4, apply *, push result 8: [3, 8]
    - Token: + (operator) -> Pop 3 and 8, apply +, push result 11: [11]

3. You have processed all the tokens, and the stack contains the final result, which is 11. 

4. Pop the result from the stack, and that's your answer: 11. 

So, in postfix notation, you evaluate the expression by repeatedly applying operators to the top elements of the stack, replacing them with the result until there's only one value left on the stack, which is the final result of the expression. This stack-based evaluation process is efficient and unambiguously handles the order of operations without the need for parentheses.

To apply this mathematical logic I created a function called "evaluate_postfix" which, evaluates the expression based on the postfix notation rules that I've already explained. 

### 6. Extra step: Add a visual GUI to the calculator

The last but also really important step would be to create a GUI(Graphical User Interface) for my Calculator. GUIs are designed to make software applications more user-friendly and accessible, allowing users to perform tasks and operations by interacting with the interface elements using a mouse, keyboard, or touchscreen. So, I just couldn't create a final project that would simply print an input line within the terminal and a result output next to a string which would be "result: ". I wanted to make an interface for my calculator, applying all of the functions that I explained above and making this interface user-friendly and interactive, just like other calculator apps that already exist(Google Calculator, Windows Calculator, phone calculator). This GUI would not be the most visually attractive interface, but it would be much better than two strings within the VScode terminal for sure. 
Everything has been completely fine until now, but how did I create the calculator's interface and make it functional at the same time? I didn't code it from scratch, I made use of the built-in module Tkinter. The Tkinter package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. The interface is quite simple. I created a window, of course with the Tkinter functions, afterwards, I created a widget in which the users would input their mathematical expressions using the TK.entry function. Then, I wrote a list of tuples named buttons. Each tuple contains the text to be displayed on the button, and its row and column position in the grid layout, setting up the color as well. You can see one of the buttons below:

('7', 1, 0, '#CCCCCC', 'black')

Finally, I created a function called "button_click" that would perform specific actions depending on which button the user would click, hence, I built a user-interactive GUI. After the mathematical expression is submitted by the user, it performs the mathematical expression submitted by the user, and afterward, it goes through all of the functions, to provide the correct answer. Creating, a PEMDAS Calculator.

To conclude, I wanted to express that, even if this final project idea was not the most creative or exciting one that I had, I decided to create the calculator, mainly because I wanted to test myself and my programming skills, I wanted to challenge myself by creating something that has already been created, but that's also a challenging project to create, it took way more time and effort than any of the problem sets I was assigned to solve.
