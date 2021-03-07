from tkinter import *

expression = ""


def press(num):
    global expression
    expression = expression + str(num)
    equation.set(expression)


def equalpress():
    try:
        global expression
        total = str(eval(expression))
        equation.set(total)
        expression = ""

    except:
        equation.set(" error ")
        expression = ""


def clear():
    global expression
    expression = ""
    equation.set("")


if __name__ == "__main__":
    window = Tk()
    window.title("My Calculator")
    equation = StringVar()
    display = Entry(window, width=33, bg="yellow", textvariable=equation)
    display.grid(row=0, column=0, columnspan=5)
    
    button1 = Button(window, text="1", command=lambda: press(1), width=5)
    button2 = Button(window, text="2", command=lambda: press(2), width=5)
    button3 = Button(window, text="3", command=lambda: press(3), width=5)
    button4 = Button(window, text="4", command=lambda: press(4), width=5)
    button5 = Button(window, text="5", command=lambda: press(5), width=5)
    button6 = Button(window, text="6", command=lambda: press(6), width=5)
    button7 = Button(window, text="7", command=lambda: press(7), width=5)
    button8 = Button(window, text="8", command=lambda: press(8), width=5)
    button9 = Button(window, text="9", command=lambda: press(9), width=5)
    button0 = Button(window, text="0", command=lambda: press(0), width=5)
    plus = Button(window, text="+", command=lambda: press("+"), width=5)
    minus = Button(window, text="-", command=lambda: press("-"), width=5)
    multiply = Button(window, text="*", command=lambda: press("*"), width=5)
    divide = Button(window, text="/", command=lambda: press("/"), width=5)
    equal = Button(window, text="=", command=equalpress, width=5)
    clear = Button(window, text="C", command=clear, width=5)
    Decimal = Button(window, text=".", command=lambda: press("."), width=5)
    
    buttons = [
        button7, button8, button9, divide, clear,
        button4, button5, button6, multiply, Button(window, text=" ", width=5),
        button1, button2, button3, minus, Button(window, text=" ", width=5),
        button0, Decimal, equal, plus, Button(window, text=" ", width=5)]

    #button-positioning
    row_index = 1
    col_index = 0

    for button in buttons:
        button.grid(row=row_index, column=col_index)
        col_index += 1
        if col_index > 4:
            row_index += 1
            col_index = 0

    window.mainloop()
