from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class GeographicCoordinates:
    latitude: float # range -90 .. 90
    longitude: float # range -180 .. 180

    def to_dms(self) -> str:
        """Convert to dms format string"""
        #TODO: implement later
        pass

@dataclass(frozen=True)
class ConversionResult:
    success: bool
    input_system: str
    conversions: dict[str, str] # system_name -> formatted_output
    error_msg: Optional[str] = None

@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    error_msg: Optional[str] = None

@dataclass(frozen=True)
class CLIArguments:
    input_system: str # -g: geographic, -m: MGRS, -u: USK-2000
    coordinates: dict # system-specific coordinates data
