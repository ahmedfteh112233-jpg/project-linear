import tkinter as tk
from gui import MatrixVisionGUI


def main():

    root = tk.Tk()

    app = MatrixVisionGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()