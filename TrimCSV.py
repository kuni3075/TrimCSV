import csv
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import japanize_matplotlib
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_file_button = tk.Button(self, text="Select CSV File", command=self.select_file)
        self.select_file_button.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.min_entry = tk.Entry(self)
        self.min_entry.grid(row=2, column=1, padx=5, pady=5)
        self.min_label = tk.Label(self, text="X Min:")
        self.min_label.grid(row=2, column=0, padx=5, pady=5)

        self.max_entry = tk.Entry(self)
        self.max_entry.grid(row=3, column=1, padx=5, pady=5)
        self.max_label = tk.Label(self, text="X Max:")
        self.max_label.grid(row=3, column=0, padx=5, pady=5)

        self.output_entry = tk.Entry(self)
        self.output_entry.grid(row=4, column=1, padx=5, pady=5)
        self.output_label = tk.Label(self, text="Output File Name:")
        self.output_label.grid(row=4, column=0, padx=5, pady=5)

        self.trim_button = tk.Button(self, text="Trim Data", command=self.trim_data)
        self.trim_button.grid(row=5, column=0, padx=5, pady=5)

        self.plot_button = tk.Button(self, text="Plot Data", command=self.plot_data)
        self.plot_button.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        self.quit_button = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit_button.grid(row=5, column=1, padx=5, pady=5)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        self.select_file_button.configure(text=self.file_path)

    def trim_data(self):
        csv_path = self.file_path
        x_min = float(self.min_entry.get())
        x_max = float(self.max_entry.get())
        output_file_path = self.output_entry.get()

        if output_file_path == "":
            output_file_path = os.path.splitext(csv_path)[0] + "_trimmed.csv"
        elif not output_file_path.endswith(".csv"):
            output_file_path += ".csv"

        with open(csv_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            reader = csv.reader(input_file)
            for i, row in enumerate(reader):
                if i == 0:
                    writer.writerow(row)
                    continue
                elif float(row[0]) < x_min:
                    continue
                elif float(row[0]) > x_max:
                    break
                else:
                    writer.writerow(row)

        self.file_path = output_file_path
        self.select_file_button.configure(text=self.file_path)

    def plot_data(self):
        csv_path = self.file_path

        x = []
        y = []
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    headers = row
                else:
                    x.append(float(row[0]))
                    y.append(float(row[1]))

        plt.plot(x, y)
        plt.xlabel(headers[0])
        plt.ylabel(headers[1])
        plt.title('CSV Data Plot')
        plt.show()

root = tk.Tk()
root.title("TrimCSV")
app = Application(master=root)
app.mainloop()