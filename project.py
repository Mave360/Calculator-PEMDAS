import re
import math
import tkinter as tk
#PEMDAS DICTIONARY TO HANDLE ORDER OF PRECEDENCE VIA KEY-VALUES
PEMDAS = {'+': 4, '-': 4, '*': 5, '/': 5, '%': 11, '√': 7, "^": 10, '(': 1, ')': 1, "[": 2, "]": 2, "{": 3, "}": 3 }

class Calculator:
    def __init__(self): #FUNCTION 1 INNIT
        self.root = tk.Tk()# creates the main application window using the tkinter library
        self.root.title("Calculator") #This sets the title of the root window to "Calculator
        self.root.resizable(False, False)  # Disable both width and height resizing
        self.expression_entry = tk.Entry(self.root, justify='right', font=('Arial', 22)) #widget is where the user can input their mathematical expressions
        self.expression_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
                #list of tuples named buttons is defined. 
        # Each tuple contains the text to be displayed on the button, 
        # and its row and column position in the grid layout. #setting up the color as well
        buttons = [
            ('7', 1, 0, '#CCCCCC', 'black'), ('8', 1, 1, '#CCCCCC', 'black'), ('9', 1, 2, '#CCCCCC', 'black'), ('/', 1, 3, '#CCCCCC', 'black'),
            ('4', 2, 0, '#CCCCCC', 'black'), ('5', 2, 1, '#CCCCCC', 'black'), ('6', 2, 2, '#CCCCCC', 'black'), ('*', 2, 3, '#CCCCCC', 'black'),
            ('1', 3, 0, '#CCCCCC', 'black'), ('2', 3, 1, '#CCCCCC', 'black'), ('3', 3, 2, '#CCCCCC', 'black'), ('-', 3, 3, '#CCCCCC', 'black'),
            ('0', 4, 0, '#CCCCCC', 'black'), ('.', 4, 1, '#CCCCCC', 'black'), (']', 4, 2, '#CCCCCC', 'black'), ('+', 4, 3, '#CCCCCC', 'black'),
            ('(', 5, 0, '#CCCCCC', 'black'), (')', 5, 1, '#CCCCCC', 'black'), ('[', 5, 2, '#CCCCCC', 'black'), ('%', 5, 3, '#CCCCCC', 'black'),
            ('{', 6, 0, '#CCCCCC', 'black'), ('}', 6, 1, '#CCCCCC', 'black'), ('√', 6, 2, '#CCCCCC', 'black'), ('^', 6, 3, '#CCCCCC', 'black'),
            ('C', 7, 1, '#CCCCCC', 'red'), ('←', 7, 2, '#CCCCCC', 'red'), ("=", 7, 3, '#CCCCCC', 'black'),
        ]

        #starts a for loop that iterates through each tuple in the buttons with their specifications
        # a lambda function is used to Specify the function to be executed when the button is clicked.
    #  It uses a lambda function to pass the text value (button label) as an argument to the self.button_click method.
    #  This allows the button_click method to know which button was clicked.
        for (text, row, col, bg_color, fg_color) in buttons:
            button = tk.Button(self.root, text=text, font=('Arial', 16), width=5, height=2, bg=bg_color, fg=fg_color, command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5)

        self.root.mainloop()

    def button_click(self, char): #FUNCTION 2
        try:
            if char == '=': #If the clicked button is '=', it signifies the user wants to evaluate the expression:
                expression = self.expression_entry.get() #It gets the expression from the expression_entry widget.

                #It checks if the expression ends with a number followed by '%' (e.g., "50%"). 
                # If so, it removes the '%' and adds division by 100 to handle percentages.
                if re.match(r'^\d+%\s*$', expression): #
                    expression = expression[:-1]  # Remove the %
                    expression = f"{expression} / 100"  # Add division by 100


                if is_valid_expression(expression): #It checks if the expression is valid using the is_valid_expression method.
                    tokens = self.unary_negation_EVALUATION(expression, self.unary_negation_TRUE_FALSE(expression)) #Tokenizes the expression
                    postfix = shunting_yard(tokens) #converts tokenized expression into postfix notation
                    evaluation = self.evaluate_postfix(postfix) #evaluates postfix converted expression
                    # updates the result in the expression_entry widget.
                    # Format the result with commas
                    formatted_result = str(evaluation)

                    self.expression_entry.delete(0, tk.END)
                    self.expression_entry.insert(0, formatted_result)
                else:
                    #If invalid, it shows "Invalid Input".
                    self.expression_entry.delete(0, tk.END)
                    self.expression_entry.insert(0, "Invalid Input")
        #If the clicked button is 'C', it clears the contents of the expression_entry widget.        
            elif char == 'C':
                self.expression_entry.delete(0, tk.END)
            #If the clicked button is '←', 
            #it removes the last character from the text in the expression_entry widget.
            elif char == '←':
                current_text = self.expression_entry.get()
                self.expression_entry.delete(0, tk.END)
                self.expression_entry.insert(0, current_text[:-1])
            #appends symbols depending on EACH OPERATOR INTRODUCED BY THE USER.
            elif char == '^':
                self.expression_entry.insert(tk.END, '^')
            elif char == '√':
                self.expression_entry.insert(tk.END, '√')
            elif char in '+-':
                if self.expression_entry.get():
                    last_char = self.expression_entry.get()[-1]
                    if last_char in '*/':
                        self.expression_entry.delete(len(self.expression_entry.get()) - 1, tk.END)
                        self.expression_entry.insert(tk.END, f' {last_char} {char} ')
                    elif last_char == '-':
                        # Check if the previous character is also a '-'
                        # If yes, treat the current '-' as a unary negation
                        self.expression_entry.delete(len(self.expression_entry.get()) - 1, tk.END)
                        self.expression_entry.insert(tk.END, ' -1 ')
                    else:
                        self.expression_entry.insert(tk.END, char)
                else:  # Handle unary negation at the start of expression
                    self.expression_entry.insert(tk.END, char)  # This is the part to add
            elif char in '*/%':
                if self.expression_entry.get():
                    last_char = self.expression_entry.get()[-1]
                    if last_char in '+-':
                        self.expression_entry.delete(len(self.expression_entry.get()) - 1, tk.END)
                        self.expression_entry.insert(tk.END, f' {last_char} {char} ')
                    else:
                        self.expression_entry.insert(tk.END, char)
            else:
                self.expression_entry.insert(tk.END, char)
        except(IndexError, ValueError):
             self.expression_entry.delete(0, tk.END)
             self.expression_entry.insert(0, "Invalid Input")

    def unary_negation_EVALUATION(self, expression, unary_negation_exists):
            expression = expression.replace(" ", "")  # Remove spaces from the input expression.
            
            if unary_negation_exists:
                VALID_DIGITS = r'(-|\+)?\d+(\.\d+)?'
                special_components = []  # Initialize a list to store components of the expression.
                
                # Define a regular expression pattern to tokenize the expression.
                pattern = r'(?:-|\+|\*|/|\(|\)|\[|\]|\{|\^|%|\d+\.\d*|\.\d+|\d+|[+\-*/\(\)\^])'


                
                # Use the regular expression pattern to find all tokens in the expression.
                tokens = re.findall(pattern, expression)
                # Iterate through the tokens.
                for token in tokens:#start COPYING HERE
                    if token == '-' and (not special_components or not re.match(VALID_DIGITS, special_components[-1])):
                        # Check if the current token is a hyphen and if either:
                        # - The list of special components is empty.
                        # - OR the last element in the list is not a digit.
                        special_components.append('-1')  # Append '-1' to the special components list.
                    else:
                        special_components.append(token)  # Append the current token to the special components list.-

                # Return the result of applying unary negation handling to the special components.
                return self.negative_1_times_following_N(special_components)
            else:
                # If unary negation does not exist, tokenize the expression using a different method.
                return tokenize(expression)


    def unary_negation_TRUE_FALSE(self, expression):
            unary_negation_exists = False  # Initialize a flag to track the existence of unary negation.
            VALID_DIGITS = r'(-|\+)?\d+(\.\d+)?'
            # Iterate through each character in the input expression.
            for char in range(len(expression)):
                if expression[char] == '-' and (char == 0 or not re.match(VALID_DIGITS, expression[char - 1])):
                # if expression[char] == '-' and (char == 0 or not expression[char - 1].isdigit()):NOT OPTIMAL CODE
                    # Check if the current character is a hyphen (-) and the following conditions are met:
                    # - It's the first character in the expression (char == 0).
                    # - OR it's not preceded by a digit (not expression[char - 1].isdigit()).
                    unary_negation_exists = True  # Set the flag to True, indicating that unary negation exists.
                    break  # Exit the loop since we found a unary negation.
            
            if unary_negation_exists:
                return True  # Return True if unary negation exists in the expression.
            else:
                return False  # Return False if unary negation does not exist in the expression.

    def negative_1_times_following_N(self, tokens):
        i = 0  # Initialize an index variable i to 0 to iterate through the list of tokens.
        VALID_DIGITS = r'(-|\+)?\d+(\.\d+)?'
        while i < len(tokens):
            # Check if the current token is "-1"
            if tokens[i] == "-1":
                # If the current token is "-1," it indicates a unary negation.
                
                # Check if there is a next token (i.e., if i + 1 is within the bounds of the list) and if it is a digit.
                if i + 1 < len(tokens) and re.match(VALID_DIGITS, tokens[i + 1]):
                    # If the next token is a digit, it means we have a negative number to handle.
                    # Convert the next token (the digit) to an integer, negate it, and convert it back to a string.
                    negated_number = str(-float(tokens[i + 1]))
                    # Replace the current token ("-1") with the negated number ("-5" for example).
                    tokens[i] = negated_number
                    # Delete the next token (the digit) since it's no longer needed.
                    del tokens[i + 1]
                    
            # Move to the next token by incrementing the index variable i.
            i += 1

        # After processing all tokens, return the modified list of tokens.
        return tokens



    def evaluate_postfix(self, tokens): #EVALUATES THE EXPRESSION FROM THE USER APPLYING MATHEMATICAL LOGIC
        stack = []

        for token in tokens: #Iterates through each character, stored into the stack and if the character is an operator 
                            #performs the following logical mathematical depending on which operator is encountered
            if token in '+-*/^√%':
                if token == '-':
                    if stack and stack[-1] == '%': #special case for subtraction by a percentage
                        stack.pop()
                        b = float(stack.pop())
                        a = float(stack.pop())
                        stack.append(str(a - (a * b * 0.01)))
                    else:
                        b = float(stack.pop())
                        a = float(stack.pop())
                        stack.append(str(a - b))

                elif token == '+':
                    if stack and stack[-1] == '%':#special case for addition by a percentage
                        stack.pop()
                        b = float(stack.pop())
                        a = float(stack.pop())
                        stack.append(str(a + (a * b * 0.01)))
                    else:
                        b = float(stack.pop())
                        a = float(stack.pop())
                        stack.append(str(a + b))
                elif token == '*':
                    if stack and stack[-1] == '%':#special case for multiplication by a percentage
                        stack.pop()
                        b = float(stack.pop())
                        a = float(stack.pop())
                        stack.append(str(a * (b * 0.01)))
                    else:
                        b = float(stack.pop())
                        a = float(stack.pop())
                        stack.append(str(a * b))
                elif token == '/':
                    if stack and stack[-1] == '%': #special case for division by a percentage
                        stack.pop()
                        b = float(stack.pop())
                        a = float(stack.pop())
                        stack.append(str(a / (b * 0.01)))
                    else:
                        b = float(stack.pop())
                        a = float(stack.pop())
                        stack.append(str(a / b))
                elif token == '^':
                    if stack and stack[-1] == '%':
                        stack.pop()
                        b_exponent = float(stack.pop())
                        a_base = float(stack.pop())
                        result = a_base ** (b_exponent * 0.01)
                        stack.append(str(result))
                    else:
                        b_exponent = float(stack.pop())
                        a_base = float(stack.pop())
                        result = a_base ** b_exponent
                        stack.append(str(result))
                elif token == '√':
                    if stack and stack[-1] == '%':
                        stack.pop()
                        b = 0.01
                    else:
                        b = 1.0
                    a = float(stack.pop())
                    result = math.sqrt(a) * b
                    stack.append(str(result))
                elif token == '%':
                    stack.append(token)
            else:
                stack.append(token)

        result = self.evaluate_grouped_parentheses(stack)
        return result

    def evaluate_grouped_parentheses(self, tokens):
        stack = []
        current_group_value = 1.0
        current_group_operator = None
        unary_negation = False  # Flag to track unary negation

        for token in tokens:
            if token in '({[':
                # Start of a new parentheses group
                if current_group_operator:
                    raise ValueError("Consecutive group operators are not allowed")
                current_group_operator = token
                stack.append(token)
            elif token in ')}]':
                # End of a parentheses group, evaluate the group
                if not current_group_operator:
                    raise ValueError("Unmatched closing group operator")
                if current_group_operator == '{' and token == '}':
                    # Evaluate the contents of the curly braces group
                    group_contents = stack.pop()  # Get the contents of the curly braces group
                    group_tokens = self.tokenize(group_contents)  # Tokenize the contents
                    group_postfix = self.shunting_yard(group_tokens)  # Convert to postfix notation
                    group_result = self.evaluate_postfix(group_postfix)  # Evaluate the contents
                    stack.append(str(group_result))  # Replace the group contents with the result
                elif current_group_operator == '[' and token == ']':
                    # Evaluate the contents of the square brackets group
                    group_contents = stack.pop()  # Get the contents of the square brackets group
                    group_tokens = self.tokenize(group_contents)  # Tokenize the contents
                    group_postfix = self.shunting_yard(group_tokens)  # Convert to postfix notation
                    group_result = self.evaluate_postfix(group_postfix)  # Evaluate the contents
                    stack.append(str(group_result))  # Replace the group contents with the result
                else:
                    raise ValueError("Mismatched group operators")
                current_group_operator = None
            else:
                if current_group_operator:
                    stack.append(token)
                else:
                    if unary_negation:
                        unary_negation = False
                        stack.append(str(-float(token)))
                    elif token != '%':  # Skip '%' when performing multiplication
                        stack.append(token)

        # Calculate the result by multiplying numeric values left in the stack
        numeric_values = [float(value) if value != '%' else 1.0 for value in stack if value not in '({[}])']
        result = 1.0
        for value in numeric_values:
            result *= value

        return result * current_group_value

def main(): #runs main function
    calculator = Calculator()
    calculator.run()


def shunting_yard(tokens): #TAKE THIS FUNCTION OUT OF THE OOP 
    operators = []  # Initialize an empty stack for operators.
    output = []  # Initialize an empty list for the output in postfix notation.

    for token in tokens:
        if token in '+-*/^√%':
            # If the token is an operator (+, -, *, /, ^, √, or %), handle operator precedence.
            
            # Check if the operators stack is not empty and if the precedence of the current token
            # is less than or equal to the precedence of the operator at the top of the stack.
            while operators and operators[-1] in '+-*/√%' and PEMDAS[token] <= PEMDAS[operators[-1]]:
                # Pop operators from the stack and append them to the output until the conditions are met.
                output.append(operators.pop())

            # Push the current token onto the operators stack.
            operators.append(token)
        elif token in '([{':
            # If the token is an opening parenthesis, bracket, or brace (e.g., (, [, {), push it onto the operators stack.
            operators.append(token)
        elif token in ')]}':
            # If the token is a closing parenthesis, bracket, or brace (e.g., ), ], }), handle matching pairs.
            
            # Pop operators from the stack and append them to the output until an opening parenthesis is encountered.
            while operators and operators[-1] not in '([{':
                output.append(operators.pop())
            
            # Check if there is a matching opening parenthesis at the top of the stack.
            if operators and operators[-1] in '([{':
                operators.pop()  # Pop and discard the matching opening parenthesis.
            else:
                raise ValueError("Mismatched parentheses, brackets, or braces")
        else:
            # If the token is not an operator or parenthesis, it's an operand (number or other).
            # Append it directly to the output.
            output.append(token)

    # After processing all tokens, any remaining operators on the stack should be popped and appended to the output.
    while operators:
        output.append(operators.pop())

    return output  # Return the list of tokens in postfix (RPN) notation.


def is_valid_expression(expression): #Checks if expression is valid using the Regex library(regular expression)
    expression = expression.replace(" ", "")
    if re.match(r'^[-^+*/()%.√\d\s\[\]{}]+$', expression) or re.match(r'^\d+%\s*$', expression):
        return expression
    else:
        return None

def tokenize(expression): #function that uses the REGEX library to tokenize the 
                          #expression accordingly with mutiple conditionals
    expression = expression.replace(" ", "")

    if "." not in expression:
        valid_components = re.findall(r'(\d+|\+|-|\*|/|\(|\)|\[|\]|\{|\^|√|%)', expression)
    elif "." in expression and " " in expression:
        valid_components = re.findall(r'(\d+\.\d+|\d+|%|\D)|[-+\*/\(\)\^]+', expression)
    elif "." in expression and " " not in expression:
        valid_components = re.findall(r'(\d+\.\d+|\d+|\.\d+|%|\D)|[-+\*/\(\)\^]+', expression)

    # Handle implicit multiplication (e.g., 2(2) -> 2*(2))
    _ = 0
    while _ < len(valid_components) - 1:
        if re.match(r'\d', valid_components[_]) and valid_components[_ + 1] in '([{':
            valid_components.insert(_ + 1, '*')
        elif valid_components[_] in ')]}' and re.match(r'\d', valid_components[_ + 1]):
            valid_components.insert(_ + 1, '*')
        _ += 1

    return valid_components



if __name__ == '__main__':
    main()

# 35.2456+(2*2)/2+√16
# -52.312+(53/5)*2+57.2
# 2-245.256^2