import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
import base64

# Flask service URL
SERVICE_URL = "http://127.0.0.1:5000"

def fetch_stock_data():
    try:
        symbol = symbol_entry.get()
        response = requests.get(f"{SERVICE_URL}/stock_data", params={"symbol": symbol})

        data = response.json()

        if "error" in data:
            messagebox.showerror("Error", data["error"])
        else:
            result_label.config(text=f"Stock Data: {data}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def calculate_moving_average():
    try:
        symbol = symbol_entry.get()
        period = int(period_entry.get())
        response = requests.get(
            f"{SERVICE_URL}/moving_average",
            params={"symbol": symbol, "period": period}
        )

        data = response.json()

        if "error" in data:
            messagebox.showerror("Error", data["error"])
        else:
            result_label.config(text=f"Moving Average: {data}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_stock_plot():
    try:
        symbol = symbol_entry.get()
        period = int(period_entry.get())
        response = requests.get(
            f"{SERVICE_URL}/stock_plot",
            params={"symbol": symbol, "period": period}
        )

        data = response.json()

        if "error" in data:
            messagebox.showerror("Error", data["error"])
        else:
            # Decode the base64 image and display it
            img_data = base64.b64decode(data['plot_url'])
            img = Image.open(io.BytesIO(img_data))
            img = ImageTk.PhotoImage(img)

            # Display the image in the Tkinter window
            plot_label.config(image=img)
            plot_label.image = img
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Stock Market Data Analysis")

# Symbol input
tk.Label(root, text="Stock Symbol:").grid(row=0, column=0, padx=10, pady=10)
symbol_entry = tk.Entry(root)
symbol_entry.grid(row=0, column=1, padx=10, pady=10)

# Period input
tk.Label(root, text="Moving Average Period:").grid(row=1, column=0, padx=10, pady=10)
period_entry = tk.Entry(root)
period_entry.grid(row=1, column=1, padx=10, pady=10)

# Fetch stock data button
fetch_button = tk.Button(root, text="Fetch Stock Data", command=fetch_stock_data)
fetch_button.grid(row=2, column=0, padx=10, pady=10)

# Calculate moving average button
moving_average_button = tk.Button(root, text="Calculate Moving Average", command=calculate_moving_average)
moving_average_button.grid(row=2, column=1, padx=10, pady=10)

# Show stock plot button
plot_button = tk.Button(root, text="Show Stock Plot", command=show_stock_plot)
plot_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Plot label for showing the graph
plot_label = tk.Label(root)
plot_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
