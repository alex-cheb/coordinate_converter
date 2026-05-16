import mgrs
from ..core.models import ValidationResult, GeographicCoordinates


# MGRS converter instance
_mgrs_converter = mgrs.MGRS()


def validate(coordinates: dict) -> ValidationResult:
    """Verifies geographic coordinates are in a proper format and limits"""
    try:
        mgrs_string = coordinates['mgrs_string']
        _mgrs_converter.toLatLon(mgrs_string) # fails if string is wrong formatted
        return ValidationResult(valid=True)
    except Exception as e:
        return ValidationResult(valid=False, error_msg=f"An error has occurred: {e}")


def to_geographic(coordinates: dict) -> GeographicCoordinates:
    """Convert the MGRS coordinates to Geographic"""
    lat, lon = _mgrs_converter.toLatLon(coordinates['mgrs_string'])
    return GeographicCoordinates(
        latitude = lat,
        longitude = lon
    )


def from_geographic(coordinates: GeographicCoordinates) -> dict:
    """Convert geographic input to MGRS"""
    lat, lon = coordinates.latitude, coordinates.longitude
    return {'mgrs_string': _mgrs_converter.toMGRS(lat, lon, 5)}
    
        
def format_output(coordinates: dict) -> str:
    """Format MGRS data for display"""
    return f"MGRS: {coordinates['mgrs_string']}"