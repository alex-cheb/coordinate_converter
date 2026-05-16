from .models import ConversionResult, ValidationResult
from .protocols import ConverterModule

_converter_registry: dict[str, ConverterModule] = {}

def register_converter(name: str, converter: ConverterModule) -> None:
    """Register a coordinate system converter module"""
    _converter_registry[name] = converter

def get_converter(name):
    """Return a requested converter by name"""
    return _converter_registry.get(name)

def get_supported_systems() -> list:
    """Return a list of supported coordinate systems"""
    return list(_converter_registry.keys())

def convert(input_system: str, coordinates: dict) -> ConversionResult:
    """Convert a requested data to all other registered systems"""
    # 1. Validate input coordinate system
    if input_system not in _converter_registry:
        return ConversionResult(
            success=False,
            input_system=input_system,
            conversions={},
            error_msg = f"Unsupported coordinate system {input_system}. Conversion supported for: {get_supported_systems()}"
        )
    
    # 2. Validate coordinates
    converter = get_converter(input_system)
    validation = converter.validate(coordinates)
    if not validation.valid:
        return ConversionResult(
        success=False,
        input_system=input_system,
        conversions={},
        error_msg=validation.error_msg
    )

    # 3. Convert to geographic (intermediate format)
    try:
        geo_coords = converter.to_geographic(coordinates)
    except Exception as e:
        return ConversionResult(
            success=False,
            input_system=input_system,
            conversions={},
            error_msg=f"Conversion to geo failed: {str(e)}"
        )

    # 4. Convert from geographic to other systems
    conversions = {}
    for system_name, system_converter in _converter_registry.items():
        if system_name == input_system:
            if input_system == "geographic":
                try:
                    if 'latitude' in coordinates:
                        from ..converters.geographic import decimal_to_dms
                        dms_coords = decimal_to_dms(coordinates['latitude'], coordinates['longitude'])
                        conversions[system_name] = f"Geographic DMS: {dms_coords}"
                    else:
                        from ..converters.geographic import parse_dms
                        lat, lon = parse_dms(coordinates['dms_string'])
                        conversions[system_name] = f"Geographic (Decimal): Lat: {lat:.4f}, Lon: {lon:.4f}"
                except Exception as e:
                    conversions[system_name] = f"ErrorAn error occured during alternating between geo types: {str(e)}\n{coordinates}"
            continue # Skip input system

        try:
            converted_coords = system_converter.from_geographic(geo_coords)
            formatted_output = system_converter.format_output(converted_coords)
            conversions[system_name] = formatted_output
        except Exception as e:
            conversions[system_name] = f"Error: {str(e)}"

    # 5. Return conversion result
    return ConversionResult(
        success=True,
        input_system=input_system,
        conversions=conversions,
        error_msg=None
    )
