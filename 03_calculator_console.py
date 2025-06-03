import math

def evaluate_expression(expression):
    try:
        allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith("__")}
        allowed_names.update({"abs": abs, "round": round}) 

        result = eval(expression, {"__builtins__": None}, allowed_names)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def show_help():
    print("\n📘 Supported Operations:")
    print(" Basic: +  -  *  /  **  %")
    print(" Trig: sin(x), cos(x), tan(x) [x in radians]")
    print("      radians(x), degrees(x)")
    print(" Logs: log(x), log10(x), log2(x)")
    print(" Exponent: exp(x), pow(x, y)")
    print(" Roots: sqrt(x)")
    print(" Constants: pi, e, tau")
    print(" Example: sin(pi/2) + log10(100) * sqrt(16)")
    print(" Type 'help' to see this again, or 'exit' to quit.\n")

def main():
    print("🧮 Scientific Calculator (Console Version)")
    print("Type 'help' to see supported operations. Type 'exit' to quit.\n")

    while True:
        expression = input(">>> ")

        if expression.lower() == 'exit':
            print("Goodbye!")
            break
        elif expression.lower() == 'help':
            show_help()
        elif expression.strip() == "":
            continue
        else:
            result = evaluate_expression(expression)
            print(f"= {result}")

if __name__ == "__main__":
    main()
