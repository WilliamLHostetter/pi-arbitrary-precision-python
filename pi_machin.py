'''
Machin's formula is a method to calculate π using the arctangent function. 
It is expressed as π = 16*arctan(1/5) - 4*arctan(1/239)

This is a Python implementation of Machin's formula to calculate π to an 
arbitrary precision. Includes a GUI dialog box to enter the input precision. 
The output is displayed in scrollable text box that can be highlighted and 
copied.
'''

import tkinter as tk
from tkinter import scrolledtext, messagebox
import decimal
from decimal import Decimal
import time



def arctan_one_over_x(x: int, unity: int) -> int:
    """
    Calculate arctan(1/x)
    arctan(1/x) = 1/x - 1/3*x**3 + 1/5*x**5 - ... (x >= 1)
    This calculates it in fixed point, using the value for one passed in
    """
    sum = xpower = unity // x
    n = 3
    sign = -1
    while 1:
        xpower = xpower // (x*x)
        term = xpower // n
        if not term:
            break
        sum += sign * term
        sign = -sign
        n += 2
    return sum


def piMachin(precision_num_digits: int) -> Decimal:
    # Use 10 guard digits internally during the calculation to avoid rounding errors in the result.
    unity = 10**(precision_num_digits + 3 + 10) 
    pi_result = (4 * (4*arctan_one_over_x(5, unity) - arctan_one_over_x(239, unity))) // (10**10)
    pi_result_str = str(pi_result)
    pi_result_str = pi_result_str[:1] + "." + pi_result_str[1:]
    decimal.getcontext().prec = precision_num_digits + 11
    pi_result_decimal = round(Decimal(pi_result_str), precision_num_digits)
    return pi_result_decimal


def readInputsAndCompute(input_window: tk.Tk, input1_var: tk.StringVar) -> None:
    input_precision_n_digits_str = input1_var.get()    
        
    try:
        precision_num_digits = int(input_precision_n_digits_str)
        assert precision_num_digits >= 0
        print("Input precision number of digits =", precision_num_digits)
    except Exception :
        error_msg = "Enter a positive integer n for precision"
        messagebox.showerror("Input Error", error_msg)
        return None
    
    start_time = time.perf_counter()
    result = piMachin(precision_num_digits)
    end_time = time.perf_counter()
    result_str = f"π = {result:.{precision_num_digits}f}"
    print(result_str)

    elapsed_time = end_time - start_time # in seconds
    if elapsed_time >= 1.0:
        elapsed_time_str = f"Computation time = {elapsed_time:.4f} s"
    else:
        elapsed_time_str = f"Computation time = {elapsed_time*1000:.4f} ms"
    print(elapsed_time_str)

    # output results to text window
    results_window = tk.Toplevel(input_window)
    results_window.title("Output")
    scrolledText = scrolledtext.ScrolledText(results_window, width=60, height=8) # width and height units are number of characters
    output_text_str = result_str + "\n\n" + elapsed_time_str
    scrolledText.insert(tk.INSERT, output_text_str)
    scrolledText.pack(fill=tk.BOTH, expand=True)
    # Right click menu for copy and select all
    menu = tk.Menu(scrolledText, tearoff=0)
    # Menu options
    menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: scrolledText.event_generate("<<Copy>>"))
    menu.add_command(label="Select All", accelerator="Ctrl+A", command=lambda: scrolledText.event_generate("<<SelectAll>>"))
    # Make menu pop up on right click event
    scrolledText.bind("<Button -3>", lambda event: menu.tk_popup(event.x_root, event.y_root))


def main() -> None:

    input_window = tk.Tk()
    input_window.title("Input")
    input_window.geometry("400x125")
    input_window.eval('tk::PlaceWindow . center')

    # declaring string variable for storing 1 input
    input1_var=tk.StringVar()

    tk.Label(input_window, text="Enter number of digits for precision", font=("Segoe UI", 14)).grid(row=0)
    entry1 = tk.Entry(input_window, font=("Arial",14), textvariable = input1_var)
    
    input_window.columnconfigure(0, weight=1)
    entry1.grid(row=1, column=0, sticky="nsew", padx=(10,10))

    button = tk.Button(input_window, text="Submit", command=lambda: readInputsAndCompute(input_window, input1_var))
    button.grid(row=5,column=0, pady=(20, 20))
    input_window.bind('<Return>', lambda event: readInputsAndCompute(input_window, input1_var))

    input_window.mainloop()


if __name__ == "__main__":
    main()

