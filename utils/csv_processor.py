import csv

# -------Helpers-----------------------
def _parse_wkt_polygon(wkt_string):
    """
    Parses a 'POLYGON ((lon lat, lon lat...))' string 
    and returns a list of (latitude, longitude) float tuples.
    """
    # 1. Strip away the WKT wrappers: "POLYGON ((" and "))"
    cleaned = wkt_string.replace("POLYGON", "").replace("(", "").replace(")", "").strip()
    
    # 2. Split by comma to separate individual coordinate pairs
    raw_points = cleaned.split(",")
    
    polygon_coords = []
    for point in raw_points:
        # Split by space to separate Longitude and Latitude
        parts = point.strip().split()
        if len(parts) == 2:
            lon = float(parts[0])
            lat = float(parts[1])
            # Swap order to (Latitude, Longitude) for TkinterMapView
            polygon_coords.append((lat, lon))
            
    return polygon_coords

def _extract_polygons_from_csv(file_path, target_column="coordinates"):
    """
    Opens the CSV, locates the specified geometry column, 
    and returns a clean list of coordinate lists.
    """
    polygons_list = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Defensive check: Ensure the column actually exists in the file
            if target_column not in reader.fieldnames:
                print(f"Error: Column '{target_column}' not found in CSV headers.")
                return []
                
            for row in reader:
                raw_wkt = row[target_column]
                clean_polygon = _parse_wkt_polygon(raw_wkt)
                
                if clean_polygon:
                    polygons_list.append(clean_polygon)
                    
        return polygons_list
        
    except Exception as e:
        print(f"Failed to process CSV file: {e}")
        return []