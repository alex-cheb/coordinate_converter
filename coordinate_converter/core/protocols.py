from typing import Protocol
from .models import GeographicCoordinates, ValidationResult


class ConverterModule(Protocol):
    def validate(self, coordinates: dict) -> ValidationResult:
        pass


    def to_geographic(self, coordinates: dict) -> GeographicCoordinates:
        pass    
    
    def from_geographic(self, coordinates: GeographicCoordinates) -> dict:
        pass    

    def format_output(self, coordinates: dict) -> str:
        pass
