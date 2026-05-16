from .core.engine import register_converter
from .converters import geographic, usk2000, mgrs
# from .converters import geographic as geographic
# from .converters import mgrs as mgrs
# from .converters import usk2000 as usk2000

def initialize_converters():
    """Register coordinate system converters"""
    register_converter("geographic", geographic)
    register_converter("mgrs", mgrs)
    register_converter("usk2000", usk2000)

# Automatically initialise converters.
initialize_converters()