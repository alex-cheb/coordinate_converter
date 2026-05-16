import coordinate_converter

from typing import List, Tuple
import tkinter.ttk as ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from ttkbootstrap.tooltip import ToolTip

TITLE = "Coordinate Converter"
THEME = "superhero"
WIDTH = 400
HEIGHT = 450
SYSTEMS = ("Geographic", "USK2000", "MGRS") # defined in root level __init___.py, convert to lowercase when passing to engine
GEO_SUBTYPES = ("Decimal", "DMS")
SYSTEM_DROPDOWN_BASE_VALUE = "Select Input System"
DMS_PLACEHOLDER = 'e.g. 40°42\'51.4"N 74°0\'21.5"W'
MGRS_PLACEHOLDER = 'e.g. 36TYT1612968670'
ERROR_LAT_LON = "Error: Please enter valid decimal numbers for latitude and longitude."
ERROR_INVALOD_COORD_SYS = f"Error: Invalid geographic coordinate type selected. Available: {', '.join(GEO_SUBTYPES)}"
ERROR_INVALID_USK_COORD = "Error: Please enter valid decimal numbers for X and Y."
ERROR_NO_INPUT_SYSTEM = "Error: No input system selected."
PADDINGS = {
    "x": 20,
    "y": 10,
}
FONT_SIZE = 11
FONT_FAMILY = "Segoe UI"
COLORS = {
    "success": "#50FA7B",
    "error": "#FF5555",
    "value": "#E0E0E0",
}

class CoordinateConverterGUI(tb.Window):
    def __init__(self):
        # super().__init__(title="Coordinate Converter", themename="superhero", size=(600, 400))
        super().__init__()
        style = tb.Style(THEME)
        self.title(TITLE)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        self.selected_system = None
        self.selected_geo_type = GEO_SUBTYPES[0]
        self.input_fields = {}

        # Create widgets and layout
        self._create_widgets()

    def _create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.input_system_dropdown = ttk.Combobox(
            self, values=SYSTEMS, state="readonly"
        )
        self.input_system_dropdown.set(SYSTEM_DROPDOWN_BASE_VALUE)
        self.input_system_dropdown.grid(row=0, column=0,
                                    sticky="ew", padx=20, pady=20)

         # Hide initial

        # ------- Geographic sub-options -------
        # Container for the toggle row — always exists, shown/hidden dynamically
        self.geo_coord_type_var = tb.StringVar(value=GEO_SUBTYPES[0])

        self.toggle_frame = tb.Frame(self)
        self.toggle_frame.grid(row=1,column=0, sticky="ew", padx=PADDINGS['x'], pady=PADDINGS['y'])
        self.toggle_frame.columnconfigure(0, weight=1)
        self.decimal_type_toggle = tb.Radiobutton(
            self.toggle_frame, text=GEO_SUBTYPES[0], value=GEO_SUBTYPES[0],
            variable=self.geo_coord_type_var
        )
        self.decimal_type_toggle.grid(row=0, column=0, sticky="w", padx=(WIDTH/3.5,0))
        self.dms_type_toggle = tb.Radiobutton(
            self.toggle_frame, text=GEO_SUBTYPES[1], value=GEO_SUBTYPES[1],
            variable=self.geo_coord_type_var
        )
        self.dms_type_toggle.grid(row=0, column=1, sticky="w", padx=(0,WIDTH/3))

        # Decimal input frame
        self.decimal_frame = tb.Frame(self)
        self.decimal_frame.grid(row=2,column=0,sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])
        self.decimal_frame.columnconfigure(1, weight=1)
        self.decimal_frame.columnconfigure(3, weight=1)
        tb.Label(self.decimal_frame, text="Latitude: ").grid(row=0, column=0, sticky="w", padx=0)
        self.decimal_lat_entry = tb.Entry(self.decimal_frame)
        self.decimal_lat_entry.grid(row=0, column=1, sticky="ew", padx=PADDINGS['x'])
        tb.Label(self.decimal_frame, text="Longitude: ").grid(row=0, column=2, sticky="w", padx=0)
        self.decimal_lon_entry = tb.Entry(self.decimal_frame)
        self.decimal_lon_entry.grid(row=0, column=3, sticky="ew", padx=PADDINGS['x'])

        # DMS input frame
        self.dms_type_frame = tb.Frame(self)
        self.dms_type_frame.grid(row=2,column=0,sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])
        tb.Label(self.dms_type_frame, text="Coordinates string: ").grid(row=0, column=0, sticky="w", padx=PADDINGS['x'])
        self.dms_coord_entry = tb.Entry(self.dms_type_frame, width=len(DMS_PLACEHOLDER)+2)
        self.dms_coord_entry.insert(0, DMS_PLACEHOLDER)
        self.dms_coord_entry.grid(row=0, column=1, sticky="ew", padx=5)

        # watching the variable for changes to trigger the appropriate handler
        self.geo_coord_type_var.trace_add("write", self._on_geo_coord_type_change)

        # Binding the dropdown change event to the handler
        self.input_system_dropdown.bind("<<ComboboxSelected>>", self._on_system_change)
        # -----------------------------------------------

        # --------- USK-2000 block ---------
        # USK-2000 input frame
        self.usk_frame = tb.Frame(self)
        self.usk_frame.grid(row=2,column=0,sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])
        self.usk_frame.columnconfigure(1, weight=1)
        self.usk_frame.columnconfigure(3, weight=1)
        tb.Label(self.usk_frame, text="X: ").grid(row=0, column=0, sticky="w", padx=0)
        self.usk_lat_entry = tb.Entry(self.usk_frame)
        self.usk_lat_entry.grid(row=0, column=1, sticky="ew", padx=PADDINGS["y"])
        tb.Label(self.usk_frame, text="Y: ").grid(row=0, column=2, sticky="w", padx=0)
        self.usk_lon_entry = tb.Entry(self.usk_frame)
        self.usk_lon_entry.grid(row=0, column=3, sticky="ew", padx=PADDINGS["y"])
        self.decimal_lon_entry.grid(row=0, column=3, sticky="ew", padx=PADDINGS["y"])

        # --------- MGRS block ---------
        # MGRS input frame
        self.mgrs_frame = tb.Frame(self)
        self.mgrs_frame.grid(row=2,column=0,sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])
        self.mgrs_frame.columnconfigure(1, weight=1)
        tb.Label(self.mgrs_frame, text="MGRS: ").grid(row=0, column=0, sticky="w", padx=PADDINGS["x"])
        self.mgrs_entry = tb.Entry(self.mgrs_frame)
        self.mgrs_entry.insert(0, MGRS_PLACEHOLDER)
        self.mgrs_entry.grid(row=0, column=1, sticky="ew", padx=5)

        for frame in (self.toggle_frame, self.decimal_frame, 
                      self.dms_type_frame, self.usk_frame, self.mgrs_frame):
            frame.grid_remove()  # Hide all input frames initially

        #------ Output -------
        self.output_text = tb.Text(self, height=10, font=(FONT_FAMILY, FONT_SIZE))
        self.output_text.grid(row=3, column=0, sticky="ews", padx=PADDINGS['x'])

        self.output_text.tag_config("value", font=(FONT_FAMILY, FONT_SIZE, "italic"),
                                    foreground=COLORS["value"])
        self.output_text.tag_config("success", font=(FONT_FAMILY, FONT_SIZE, "bold"),
                                    foreground=COLORS["success"])
        self.output_text.tag_config("error", font=(FONT_FAMILY, FONT_SIZE, "bold"),
                                    foreground=COLORS["error"])

        # ------ Controls -------
        self.convert_button = tb.Button(self, text="Convert", command=self._on_convert)
        self.convert_button.config(state="disabled")
        self.convert_button.grid(row=4, column=0, pady=PADDINGS['y'], sticky="ews", padx=PADDINGS['x'])

    
    def _on_system_change(self, event=None):
        self._hide_all_input_frames()

        selected = self.input_system_dropdown.get()
        if not selected or selected == SYSTEM_DROPDOWN_BASE_VALUE:
            self.convert_button.config(state="disabled")
            return
        else:            
            self.convert_button.config(state="normal")

        if selected == SYSTEMS[0]:  # Geographic
            self.toggle_frame.grid(row=1, column=0, sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])
            self._on_geo_coord_type_change()  # Trigger to show the correct sub-toggle
        elif selected == SYSTEMS[1]:  # USK-2000
            self.usk_frame.grid(row=2, column=0, sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])
        elif selected == SYSTEMS[2]:  # MGRS
            self.mgrs_frame.grid(row=2, column=0, sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])
        else:
            self._hide_all_input_frames()

    def _on_geo_coord_type_change(self, *args):
        selected_type = self.geo_coord_type_var.get()
        if selected_type == GEO_SUBTYPES[0]:
            self.dms_type_frame.grid_remove()
            self.decimal_frame.grid(row=2, column=0, sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])
        elif selected_type == GEO_SUBTYPES[1]:
            self.decimal_frame.grid_remove()
            self.dms_type_frame.grid(row=2, column=0, sticky='ew', padx=PADDINGS['x'], pady=PADDINGS['y'])

    def _hide_all_input_frames(self):
        for frame in (self.toggle_frame, 
                      self.decimal_frame, 
                      self.dms_type_frame, 
                      self.usk_frame,
                      self.mgrs_frame):
            frame.grid_remove()

    def _on_convert(self):
        self.convert_button.config(state="disabled")  # Disable button to prevent multiple clicks
        selected_system = self.input_system_dropdown.get()
        if selected_system == SYSTEMS[0]:  # Geographic
            coord_type = self.geo_coord_type_var.get()
            if coord_type == GEO_SUBTYPES[0]:
                try:
                    lat = float(self.decimal_lat_entry.get())
                    lon = float(self.decimal_lon_entry.get())
                    coordinates = {"latitude": lat, "longitude": lon}
                except ValueError:
                    self.output_text.delete(1.0, END)
                    self.output_text.insert(END, ERROR_LAT_LON)
                    return
            elif coord_type == GEO_SUBTYPES[1]:
                dms_string = self.dms_coord_entry.get()
                coordinates = {"dms_string": dms_string}
            else:
                self.output_text.delete(1.0, END)
                self.output_text.insert(END, ERROR_INVALOD_COORD_SYS)
                return

        elif selected_system == SYSTEMS[1]:  # USK-2000
            try:
                x = float(self.usk_lat_entry.get())
                y = float(self.usk_lon_entry.get())
                coordinates = {"x": x, "y": y}
            except ValueError:
                self.output_text.delete(1.0, END)
                self.output_text.insert(END, ERROR_INVALID_USK_COORD)
                return

        elif selected_system == SYSTEMS[2]:  # MGRS
            mgrs_string = self.mgrs_entry.get()
            coordinates = {"mgrs_string": mgrs_string}

        else:
            self.output_text.delete(1.0, END)
            self.output_text.insert(END, ERROR_NO_INPUT_SYSTEM)
            return
        from ..core.engine import convert

        result = convert(selected_system.lower(), coordinates)

        self.convert_button.config(state="normal")  # Re-enable button
        self._display_result(result)

    def _display_result(self, result):
        if result.success:
            self.output_text.delete(1.0, END)  # Clear previous output
            for system, formatted_output in result.conversions.items():
                for line in formatted_output.splitlines():
                    if ": " in line:
                        label, value = line.split(": ", 1)
                        self.output_text.insert(END, f"{label}: ", "success")
                        self.output_text.insert(END, f"{value}\n", "value")
                    else:
                        self.output_text.insert(END, f"{line}\n", "success")
        else:
                self.output_text.delete(1.0, END)  # Clear previous output
                self.output_text.insert(END, "Error: ", "error")
                self.output_text.insert(END, f"{result.error_msg}", "value")


if __name__ == "__main__":
    app = CoordinateConverterGUI()
    app.mainloop()