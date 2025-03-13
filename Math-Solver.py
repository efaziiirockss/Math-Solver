import math

def smart_calculator():
    # Display welcome message
    print('''
          Welcome to Math Solver! 
      Type: Help for Useful Commands''')
    
    # Dictionary to store user-defined variables
    variables = {}
    # List to store calculation history
    history = []
    
    while True:
        # Get user input and remove whitespace
        user_input = input("\n> ").strip()
        
        # Handle exit commands
        if user_input.lower() in ['exit', 'quit', 'q']:
            print('Thanks for using this math solver! ')
            break
            
        # Display help menu    
        elif user_input.lower() == 'help':
            print("""
Commands:
- Basic operations: +, -, *, /, ^ (power), % (modulo)
- Functions: sin, cos, tan, sqrt, log, root
- Constants: pi, e
- Variables: x = 10, then use x in expressions
- 'history' to see previous calculations
- 'exit' to quit
            """)
            
        # Display calculation history    
        elif user_input.lower() == 'history':
            if history:
                for i, (expr, result) in enumerate(history, 1):
                    print(f"{i}. {expr} = {result}")
            else:
                print("No calculations yet.")
                
        # Clear all variables and history    
        elif user_input.lower() == 'clear':
            variables.clear()
            history.clear()
            print("Variables and history cleared.")        
        
        # Skip empty input
        elif not user_input:
            continue
            
        else:
            try:
                # Handle variable assignment operations
                if '=' in user_input and '==' not in user_input:
                    var_name, expr = user_input.split('=', 1)
                    var_name = var_name.strip()
                    
                    # Replace variables with their stored values
                    for name, value in variables.items():
                        expr = expr.replace(name, str(value))
                    
                    # Process and evaluate the expression    
                    expr = prepare_expression(expr)
                    result = eval(expr)
                    variables[var_name] = result
                    print(f"{var_name} = {result}")
                    history.append((user_input, result))
                    
                else:
                    # Handle regular calculations
                    expression = user_input
                    # Replace variables with their values
                    for name, value in variables.items():
                        expression = expression.replace(name, str(value))
                        
                    # Process and evaluate the expression
                    expression = prepare_expression(expression)
                    result = eval(expression)
                    print(f"= {result}")
                    history.append((user_input, result))
                    
            except Exception as e:
                print(f"Error: {e}")

def prepare_expression(expr):
    """
    Prepare the expression for evaluation by converting mathematical notations
    and handling special functions.
    Args:
        expr (str): The mathematical expression to prepare.
    Returns:
        str: Processed expression ready for evaluation.
    """
    # Replace the power operator '^' with Python's exponentiation operator '**'
    expr = expr.replace('^', '**')
    
    # Check if the expression contains the root function call 'root('
    if 'root(' in expr:
        # Split the expression into parts using 'root(' as the delimiter
        parts = expr.split('root(')
        # Loop through the parts beginning from the first occurrence after splitting
        for i in range(1, len(parts)):
            # Check if the current part contains a comma, which separates the arguments
            if ',' in parts[i]:
                # Split the part at the first comma to extract the base value and the root degree
                num, root = parts[i].split(',', 1)
                # Further split to remove the trailing ')' and any extra whitespace from the root degree
                root = root.split(')')[0].strip()
                # Replace the root function call (e.g., root(16,2)) with Python's equivalent using pow()
                expr = expr.replace(f'root({num},{root})', f'pow({num}, 1/{root})')
    
    # Replace sin( with math.sin(math.radians( so that angles in degrees are converted to radians
    expr = expr.replace('sin(', 'math.sin(math.radians(')
    # Replace cos( with math.cos(math.radians( for the same reason as above
    expr = expr.replace('cos(', 'math.cos(math.radians(')
    # Replace tan( with math.tan(math.radians( for the same reason as above
    expr = expr.replace('tan(', 'math.tan(math.radians(')
    # Replace sqrt( with math.sqrt( to directly use math module's square root function
    expr = expr.replace('sqrt(', 'math.sqrt(')
    # Replace log( with math.log( to use math module's natural log function
    expr = expr.replace('log(', 'math.log(')
    
    # Loop through the trigonometric functions to ensure correct closure of parentheses
    for func in ['sin', 'cos', 'tan']:
        # Check if the math function call (e.g., math.sin(math.radians() exists in the expression
        if f'math.{func}(math.radians(' in expr:
            # Count the number of times the function call pattern appears (i.e., the number of open calls)
            open_count = expr.count(f'math.{func}(math.radians(')
            # Count the overall closing parentheses in the expression
            close_count = expr.count(')')
            # Each such function call requires two closing parentheses. Calculate the total needed.
            needed = open_count * 2
            # If there are fewer closing parentheses than needed, append the missing ones at the end
            if close_count < needed:
                expr += ')' * (needed - close_count)
    
    # Replace the place-holder 'pi' with the numerical value of pi from the math module
    expr = expr.replace('pi', str(math.pi))
    # Replace the place-holder 'e' with the numerical value of e from the math module
    expr = expr.replace('e', str(math.e))
    
    # Return the fully processed expression, now ready to be evaluated by eval()
    return expr

if __name__ == "__main__":
    smart_calculator()