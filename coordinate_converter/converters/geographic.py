import re
from ..core.models import ValidationResult, GeographicCoordinates

def detect_format(input_str: str) -> str:
    """Returns decimal or dms based on the input"""
    return 'dms' if '°' in input_str else 'decimal'

def parse_decimal(input_str: str) -> tuple[float, float]:
    """Parses geographic coords input given in decimal format"""
    lat, lon = input_str.replace(',', ' ').split()
    lat = float(lat)
    lon = float(lon)
    return (lat, lon)

def parse_dms(input_str: str) -> tuple[float, float]:
    """Parses geographic coords provided in degrees, minutes, seconds format"""
    pattern = r'(\d+)°(\d+)\'([\d.]+)"([NSEW])'
    lat, lon = (re.match(pattern, s).groups() for s in input_str.split())
    return (dms_to_decimal(lat), dms_to_decimal(lon))
    

def dms_to_decimal(dms_tuple: tuple) -> float:
    """Helper method to convert DMS"""
    # degrees + minutes/60 + seconds/3600, apply sign based on direction (S/W = negative)
    # unpack values
    degrees, minutes, seconds, direction = dms_tuple
    # convert strings to floats
    degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
    # calculate decimal value
    decimal = degrees + minutes/60 + seconds/3600
    
    # S and W direction gives a negative sign
    if direction in ("S", "W"):
        decimal = -decimal
    return decimal

def decimal_to_dms(latitude: float, longitude: float) -> str:
    """Helper method to convert decimal"""
    # degrees (int), minutes (int), seconds (float)
    def convert(value, lat_or_lon):
        if lat_or_lon == "lat":
            direction = 'N' if value >= 0 else 'S'
        else:
            direction = 'E' if value >= 0 else 'W'
        value = abs(value)
        degrees = int(value)
        min_decimal = (value - degrees) * 60
        mins = int(min_decimal)
        seconds = (min_decimal - mins) * 60

        return f"{degrees}°{mins}\'{seconds:.1f}\"{direction}"
    
    lat_dms = convert(latitude, 'lat')
    lon_dms = convert(longitude, 'lon')
    return f"{lat_dms} {lon_dms}"

def validate(coordinates: dict) -> ValidationResult:
    """Verifies geographic coordinates are in a proper format and limits"""
    try:
        # lat, lon = coordinates['latitude'], coordinates['longitude']

        if 'dms_string' in coordinates:
            from .geographic import parse_dms
            lat, lon = parse_dms(coordinates['dms_string'])
        else:
            lat, lon = coordinates['latitude'], coordinates['longitude']

        if not (-90<= lat <= 90):
            return ValidationResult(valid=False, error_msg=f"Latitude {lat} is not within expected boundaries")
        if not (-180<= lon <= 180):
            return ValidationResult(valid=False, error_msg=f"Longitude {lon} is not within expected boundaries")

        return ValidationResult(valid=True)
    except Exception as e:
        return ValidationResult(valid=False, error_msg=f"An error has occurred: {e}")

def to_geographic(coordinates: dict) -> GeographicCoordinates:
    """Already geographic. TO stick to the protocol"""
    # return GeographicCoordinates(
    #     latitude=coordinates["latitude"],
    #     longitude=coordinates["longitude"]
    # )
    # Handle DMS string format
    if 'dms_string' in coordinates:
        lat, lon = parse_dms(coordinates['dms_string'])
    else:
        lat, lon = coordinates['latitude'], coordinates['longitude']
    
    return GeographicCoordinates(latitude=lat, longitude=lon)

def from_geographic(coordinates: GeographicCoordinates) -> dict:
    """Already geographic. Transforms to dictionary"""
    return {
        "latitude":coordinates.latitude,
        "longitude":coordinates.longitude
    }
        
def format_output(coordinates: dict) -> str:
    """Format both dms and decimal"""
    lat = coordinates["latitude"]
    lon = coordinates["longitude"]
    dms = decimal_to_dms(lat, lon)
    return f"Geo (Decimal): Lat: {lat:.6f}, Lon: {lon:.6f}\nGeo (DMS): {dms}"
    