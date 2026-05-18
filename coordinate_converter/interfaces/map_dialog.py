import ttkbootstrap as tb
# from tkinterweb import HtmlFrame
from tkintermapview import TkinterMapView

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
                                        