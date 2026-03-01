import tkinter as tk
from tkinter import filedialog
from backend.predict import predict_image


def upload():

    file = filedialog.askopenfilename()

    result = predict_image(file)

    label.config(text=result)


root = tk.Tk()

root.title("Breast Cancer Detection")

button = tk.Button(root,text="Upload Mammogram",command=upload)

button.pack()

label = tk.Label(root,text="Result")

label.pack()

root.mainloop()