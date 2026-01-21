import tkinter as tk
from tkinter import messagebox, filedialog
import os
import ee
import pandas as pd

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception as e:
    print(f"Failed to initialize Earth Engine: {e}")
    exit()

# Precipitation data processing functions
def process_year(start_year, end_year, model_name, point, output_folder_daily, output_folder_monthly, log_callback):
    log_callback(f"Processing data for model: {model_name}, years: {start_year}-{end_year}")
    log_callback(f"Saving daily data to: {output_folder_daily}")
    log_callback(f"Saving monthly data to: {output_folder_monthly}")
    
    # Mock data for testing file saving
    daily_data = pd.DataFrame({"Date": ["2023-01-01", "2023-01-02"], "Precipitation": [10, 12]})
    monthly_data = pd.DataFrame({"Month": ["2023-01"], "Total_Precipitation": [22]})

    # Ensure output directories exist
    os.makedirs(output_folder_daily, exist_ok=True)
    os.makedirs(output_folder_monthly, exist_ok=True)

    # Define file paths
    daily_path = os.path.join(output_folder_daily, f"{model_name}_{start_year}_{end_year}_daily.csv")
    monthly_path = os.path.join(output_folder_monthly, f"{model_name}_{start_year}_{end_year}_monthly.csv")

    try:
        daily_data.to_csv(daily_path, index=False)
        log_callback(f"Daily data saved to {daily_path}")
    except Exception as e:
        log_callback(f"Error saving daily data: {e}")

    try:
        monthly_data.to_csv(monthly_path, index=False)
        log_callback(f"Monthly data saved to {monthly_path}")
    except Exception as e:
        log_callback(f"Error saving monthly data: {e}")

class PrecipitationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Precipitation Data Processor")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Initialize variables
        self.station_name = tk.StringVar()
        self.latitude = tk.DoubleVar()
        self.longitude = tk.DoubleVar()
        self.model_name = tk.StringVar()
        self.scenario_name = tk.StringVar()
        self.start_year = tk.IntVar()
        self.end_year = tk.IntVar()

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Station name input
        self.create_label("Enter Station Name:", 0, 0)
        self.create_entry(self.station_name, 0, 1)

        # Latitude and Longitude inputs
        self.create_label("Enter Latitude:", 1, 0)
        self.create_entry(self.latitude, 1, 1)

        self.create_label("Enter Longitude:", 2, 0)
        self.create_entry(self.longitude, 2, 1)

        # Model selection dropdown
        self.create_label("Choose Model:", 3, 0)
        model_options = [
            'ACCESS-CM2', 'ACCESS-ESM1-5', 'BCC-CSM2-MR', 'CESM2', 'CESM2-WACCM', 'CMCC-CM2-SR5',
            'CMCC-ESM2', 'CNRM-CM6-1', 'CNRM-ESM2-1', 'CanESM5', 'EC-Earth3', 'EC-Earth3-Veg-LR',
            'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'GISS-E2-1-G', 'HadGEM3-GC31-LL', 'HadGEM3-GC31-MM',
            'IITM-ESM', 'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM',
            'MIROC-ES2L', 'MIROC6', 'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NESM3',
            'NorESM2-LM', 'NorESM2-MM', 'TaiESM1', 'UKESM1-0-LL'
        ]
        self.create_option_menu(self.model_name, model_options, 3, 1)

        # Scenario selection dropdown
        self.create_label("Choose Scenario:", 4, 0)
        scenario_options = ['historical', 'ssp245', 'ssp585']
        self.create_option_menu(self.scenario_name, scenario_options, 4, 1)

        # Year range selection
        self.create_label("Start Year:", 5, 0)
        self.create_entry(self.start_year, 5, 1)

        self.create_label("End Year:", 6, 0)
        self.create_entry(self.end_year, 6, 1)

        # Choose output folders for daily and monthly data
        self.create_label("Choose Output Folder for Daily Data:", 7, 0)
        self.create_button("Browse", self.select_daily_folder, 7, 1)

        self.create_label("Choose Output Folder for Monthly Data:", 8, 0)
        self.create_button("Browse", self.select_monthly_folder, 8, 1)

        # Process Button
        self.create_button("Process Data", self.process_data, 9, 0, colspan=2)

        # Console log display
        self.log_text = tk.Text(self.frame, wrap="word", height=15, state="disabled", bg="#e6e6e6", font=("Courier", 10))
        self.log_text.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def create_label(self, text, row, column):
        label = tk.Label(self.frame, text=text, font=("Arial", 12), bg="#f0f0f0")
        label.grid(row=row, column=column, sticky="w", padx=10, pady=5)

    def create_entry(self, variable, row, column):
        entry = tk.Entry(self.frame, textvariable=variable, font=("Arial", 12), width=30)
        entry.grid(row=row, column=column, padx=10, pady=5)

    def create_option_menu(self, variable, options, row, column):
        menu = tk.OptionMenu(self.frame, variable, *options)
        menu.config(font=("Arial", 12))
        menu.grid(row=row, column=column, padx=10, pady=5)

    def create_button(self, text, command, row, column, colspan=1):
        button = tk.Button(self.frame, text=text, font=("Arial", 12), bg="#007bff", fg="white", command=command)
        button.grid(row=row, column=column, columnspan=colspan, padx=10, pady=10, sticky="ew")
        return button

    def select_daily_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.daily_folder = folder_selected
            self.log(f"Daily data will be saved to: {self.daily_folder}")

    def select_monthly_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.monthly_folder = folder_selected
            self.log(f"Monthly data will be saved to: {self.monthly_folder}")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def process_data(self):
        station_name = self.station_name.get()
        latitude = self.latitude.get()
        longitude = self.longitude.get()
        model_name = self.model_name.get()
        scenario_name = self.scenario_name.get()
        start_year = self.start_year.get()
        end_year = self.end_year.get()

        # Validate inputs
        if not station_name or not latitude or not longitude or not model_name or not scenario_name:
            messagebox.showerror("Input Error", "Please fill in all the fields.")
            return

        if start_year < 1990 or end_year > 2100 or start_year > end_year:
            messagebox.showerror("Year Error", "Please choose a valid year range.")
            return

        if not hasattr(self, 'daily_folder') or not hasattr(self, 'monthly_folder'):
            messagebox.showerror("Folder Error", "Please select both daily and monthly output folders.")
            return

        # Convert coordinates to ee.Geometry.Point
        point = ee.Geometry.Point([longitude, latitude])

        # Call the data processing function
        try:
            process_year(
                start_year, end_year, model_name, point, self.daily_folder, self.monthly_folder, self.log
            )
            self.log("Data processing completed successfully.")
        except Exception as e:
            self.log(f"An error occurred during data processing: {e}")
            messagebox.showerror("Processing Error", f"An error occurred: {e}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PrecipitationApp(root)
    root.mainloop()