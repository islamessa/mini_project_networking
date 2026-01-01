import tkinter as tk
from tkinter import messagebox

def run_calculator():
    def calculate():
        try:
            a = int(entry1.get())
            b = int(entry2.get())
            result.set(a + b)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    root = tk.Tk()
    root.title("Calculator")
    root.geometry("300x200")
    root.resizable(False, False)

    result = tk.StringVar(value="0")

    tk.Label(root, text="First number").pack(pady=5)
    entry1 = tk.Entry(root)
    entry1.pack()

    tk.Label(root, text="Second number").pack(pady=5)
    entry2 = tk.Entry(root)
    entry2.pack()

    tk.Button(root, text="Add", command=calculate).pack(pady=10)

    tk.Label(root, text="Result").pack()
    tk.Label(root, textvariable=result, font=("Arial", 14, "bold")).pack()

    root.mainloop()


# Only runs if this file is executed directly
if __name__ == "__main__":
    run_calculator()
