import ttkbootstrap as tb
from pathlib import Path
from tkinter import filedialog, messagebox
from tkintermapview import TkinterMapView
from utils import csv_processor as cp

TITLE = "Coordinate Converter - Map Display"
FONT_FAMILY = "Segoe UI"
FONT_SIZE = 10
HEIGHT = 600
WIDTH = 800



class MapWindow(tb.Toplevel):
    def __init__(self, parent, lat=0, lon=0):
        super().__init__(parent)
        self.title(TITLE)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH-200, HEIGHT-150)
        self.lat = lat
        self.lon = lon
        self.csv_path = None
        self.polygons = []
        self.polygons_visible = False
        #self.grab_set()  # Make this window modal
        self.create_widgets()

    def create_widgets(self):
        # ------- Header -------
        header = tb.Frame(self)
        header.grid(row=0, column=0, sticky="ew")
        self.coord_text = f"Latitude: {self.lat}, Longitude: {self.lon}"
        self.coord_label = tb.Label(header, text=self.coord_text, font=("Helvetica", 11))
        self.coord_label.grid(row=0, column=0, padx=10, pady=10)
        tb.Button(header, text="✕ Close", command=self.destroy,
                   bootstyle="danger-outline").grid(row=0, column=1, padx=10, pady=10)
        tb.Button(header, text="Load CSV", command=self._on_load_csv,
                  bootstyle="secondary").grid(row=0, column=2, padx=10, pady=10)
        tb.Button(header, text="Show/Hide", command=self._on_show_polygons,
                  bootstyle="success").grid(row=0, column=3, padx=10, pady=10)
        
        # ------- Map -------
        # Simple, lightweight map widget
        self.map_widget = TkinterMapView(self, corner_radius=10)
        self.map_widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.map_widget.set_zoom(12)
        self.map_widget.set_position(self.lat, self.lon)
        self.map_widget.set_marker(self.lat, self.lon, text="Target Coordinates")

    def update_position(self, lat, lon):
        self.lat = lat
        self.lon = lon
        # Update the map position and marker
        self.coord_label.config(text=f"Latitude: {self.lat}, Longitude: {self.lon}")
        self.map_widget.set_position(self.lat, self.lon)
        self.map_widget.delete_all_marker()
        self.map_widget.set_marker(self.lat, self.lon, text="Target Coordinates")
    
    def _on_load_csv(self):
        """Opens a dialogue for CSV selection"""
        file_path = filedialog.askopenfilename(
            title="Open CSV", 
            filetypes=[("CSV Files", "*.csv")])
        
        if not file_path:
            return
        
        try:
            self.csv_path = Path(file_path)
            self.polygons = cp._extract_polygons_from_csv(self.csv_path)
            tb.Label(self, text=f"{len(self.polygons)} polygons from {self.csv_path.name} available", font=("Helvetica", 10)).grid(row=2, column=0, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f'Failed to load CSV: {e}')

    def _on_show_polygons(self):
        # Placeholder for polygon display functionality
        if not self.polygons:
            tb.Label(self, text=f"No border data is loaded", font=("Helvetica", 10), foreground="red").grid(row=2, column=0, padx=10, pady=5)
            return
        if not self.polygons_visible:
            self.polygons_visible = True
            for polygon_points in self.polygons:
                self.map_widget.set_polygon(
                    position_list=polygon_points,
                    fill_color=None,              # "None" keeps the inside completely clear/transparent
                    outline_color="#f03e3e",      # A nice clean tactical red hex color
                    border_width=2,               # Thickness of the outline border line
                command=None                  # Optional callback function if a user clicks the polygon
        )
        else:
            self.polygons_visible = False
            self.map_widget.delete_all_polygon()
                                        