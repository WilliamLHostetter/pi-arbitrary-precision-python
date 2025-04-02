'''
The Chudnovsky algorithm is a fast method for calculating the digits of π, based 
on Ramanujan's π formulae. It was published by the Chudnovsky brothers in 1988 
and is known for its efficiency in computing π to a high number of decimal 
places. 

This is a direct Python implementation of the Chudnovsky algorithm to calculate 
π to an arbitrary precision. Includes a GUI dialog box to enter the input 
precision. The output is displayed in scrollable text box that can be 
highlighted and copied.

For reference, the first 100 digits of π are
3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
'''

import tkinter as tk
from tkinter import scrolledtext, messagebox
import math
import decimal
import time



def piChudnovsky(precision_num_digits):
    decimal_precision = precision_num_digits + 2
    decimal.getcontext().prec = decimal_precision
    total = decimal.Decimal(0)

    for k in range(precision_num_digits):
        a_k = decimal.Decimal(((-1)**k)*((math.factorial(6*k))*(545140134*k + 13591409)) /
                (math.factorial(3*k)*(math.factorial(k)**3)*((decimal.Decimal(640320))**(decimal.Decimal(3*k + 3/2)))))
        total += a_k
    
    sum_result = decimal.Decimal(12) * total 
    pi_result = decimal.Decimal(1) / sum_result
    pi_result_rounded = round(pi_result, precision_num_digits)
    return pi_result_rounded



def readInputsAndCompute(input_window, input1_var):
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
    result = piChudnovsky(precision_num_digits)
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


def main():

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

    input_window.mainloop()


if __name__ == "__main__":
    main()
