from pyproj import CRS, Transformer
from ..core.models import ValidationResult, GeographicCoordinates

# Reference coordinate systems
_wgs84 = CRS.from_epsg(4326) # WGS84, geographic
_usk2000 = CRS.from_epsg(5561) # USK-2000

# Create transformer for conversions
_transformer_to_geo = Transformer.from_crs(_usk2000, _wgs84, always_xy=True)
_transformer_from_geo = Transformer.from_crs(_wgs84, _usk2000, always_xy=True)


def validate(coordinates: dict) -> ValidationResult:
    """Verifies geographic coordinates are in a proper format and limits"""
    try:
        # USK-2000 coordinates are valid in Ukraine (approx 0-900km east, 0-700km north)
        x, y = coordinates['x'], coordinates['y']
        if not (0<= x <= 900000 and 0 <= y <= 700000):
            return ValidationResult(valid=False, error_msg=f"The coordinates {(x, y)} are out of expected range (Ukraine)")
        return ValidationResult(valid=True)
    except Exception as e:
        return ValidationResult(valid=False, error_msg=f"An error has occurred: {e}")


def to_geographic(coordinates: dict) -> GeographicCoordinates:
    """Convert the USK-2000 coordinates to Geographic"""
    lon, lat = _transformer_to_geo.transform(coordinates['x'], coordinates['y'])
    return GeographicCoordinates(
        latitude = lat,
        longitude = lon
    )


def from_geographic(coordinates: GeographicCoordinates) -> dict:
    """Convert geographic input to USK-2000"""
    x, y = _transformer_from_geo.transform(coordinates.longitude, coordinates.latitude)
    return {'x':x, 'y':y}
    
        
def format_output(coordinates: dict) -> str:
    """Format USK-2000 data for display"""
    return f"USK-2000: X={coordinates['x']:.2f}, Y={coordinates['y']:.2f}"