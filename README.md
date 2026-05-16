# Coordinate Converter

A Python application for converting geographic coordinates between different coordinate systems. Supports Geographic (latitude/longitude), MGRS (Military Grid Reference System), and USK-2000 (Ukrainian Spatial Coordinate System 2000) with both command-line and graphical user interfaces.

## Features

- **Multiple Coordinate Systems**: Convert between Geographic, MGRS, and USK-2000
- **Flexible Input Formats**: 
  - Geographic: Decimal degrees (`49.0000, 37.0000`) or DMS (`49°00'00.1"N 37°00'00.1"E`)
  - MGRS: Standard MGRS strings
  - USK-2000: Ukrainian coordinate format
- **Dual Interfaces**: 
  - Command-line interface (CLI) for scripting and automation
  - Graphical user interface (GUI) with Tkinter and ttkbootstrap
- **Simultaneous Conversion**: Convert to all supported systems in a single operation
- **Extensible Architecture**: Easy to add new coordinate systems
- **Property-Based Testing**: Comprehensive correctness properties with Hypothesis

## Installation

### Prerequisites
- Python 3.10 or higher
- pip or similar package manager

### Quick Start

```bash
# Clone or download the repository
cd coordinate-converter

# Install with production dependencies
pip install -e .

# Or install with development dependencies (for testing)
pip install -e ".[dev]"
```

## Usage

### Command-Line Interface (CLI)

Convert geographic coordinates (decimal format):
```bash
coordinate-converter-cli -g 49.0 37.0
```

Convert geographic coordinates (DMS format):
```bash
coordinate-converter-cli -g "49°00'00.1\"N 37°00'00.1\"E"
```

Convert MGRS coordinates:
```bash
coordinate-converter-cli -m "33UXP1234567890"
```

Convert USK-2000 coordinates:
```bash
coordinate-converter-cli -u "1234567.89 9876543.21"
```

### Graphical User Interface (GUI)

Launch the GUI application:
```bash
coordinate-converter-gui
```

The GUI provides:
- Dropdown selector for input coordinate system
- Dynamic input fields that adapt to the selected system
- Format toggle for geographic coordinates (Decimal/DMS)
- Real-time conversion to all other systems
- Error display for invalid inputs

## Output Format

All conversions display results in plain text with system labels:

```
Geographic (Decimal): Lat: 49.000028, Lon: 37.000028
Geographic (DMS): 49°00'00.1"N 37°00'00.1"E
MGRS: 33UXP1234567890
USK-2000: X=1234567.89, Y=9876543.21
```

## Architecture

### Modular Design

The application follows a clean separation of concerns:

- **Core Engine** (`core/`): Conversion orchestration and registry
- **Converters** (`converters/`): System-specific conversion logic
- **Interfaces** (`interfaces/`): CLI and GUI implementations
- **Tests** (`tests/`): Property-based and unit tests

### Functional Approach

Business logic uses pure functions without state:
- Easier to test and reason about
- Better composability
- No hidden side effects

### Extensibility

Adding new coordinate systems is straightforward:

1. Create a new converter module in `converters/`
2. Implement the required functions: `validate()`, `to_geographic()`, `from_geographic()`, `format_output()`
3. Register the converter in the initialization module

## Supported Coordinate Systems

### Geographic (WGS84)
- **Decimal Format**: `49.0000, 37.0000` or `49.0000 37.0000`
- **DMS Format**: `49°00'00.1"N 37°00'00.1"E`
- **Range**: Latitude [-90, 90], Longitude [-180, 180]

### MGRS (Military Grid Reference System)
- **Format**: `33UXP1234567890`
- **Precision**: 1 meter (10-digit format)

### USK-2000 (Ukrainian Spatial Coordinate System 2000)
- **Format**: `X=1234567.89, Y=9876543.21`
- **Coverage**: Ukraine and surrounding areas
- **Precision**: Centimeters

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_converters.py

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov=coordinate_converter --cov-report=html
```

### Project Structure

```
coordinate-converter/
├── core/
│   ├── __init__.py
│   ├── engine.py           # Conversion engine and registry
│   ├── models.py           # Data models (dataclasses)
│   └── protocols.py        # ConverterModule protocol
├── converters/
│   ├── __init__.py
│   ├── geographic.py       # Geographic converter
│   ├── mgrs.py             # MGRS converter
│   └── usk2000.py          # USK-2000 converter
├── interfaces/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   └── gui.py              # Graphical user interface
├── tests/
│   ├── __init__.py
│   ├── test_properties.py  # Property-based tests
│   ├── test_converters.py  # Unit tests
│   ├── test_cli.py         # CLI tests
│   └── test_gui.py         # GUI tests
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Dependencies

### Production
- **mgrs** (>=1.4.0): MGRS coordinate conversions
- **pyproj** (>=3.4.0): Coordinate system transformations
- **ttkbootstrap** (>=1.10.0): Modern Tkinter themes

### Development
- **pytest** (>=7.0.0): Testing framework
- **hypothesis** (>=6.0.0): Property-based testing
- **pytest-cov** (>=4.0.0): Coverage reporting

## Correctness Properties

The application is validated using property-based testing with Hypothesis:

1. **Round-trip conversion**: Converting to another system and back preserves coordinates within tolerance
2. **Conversion completeness**: All other systems are present in output
3. **Invalid input handling**: Descriptive error messages for invalid coordinates
4. **Output format**: Plain text with labels and correct precision
5. **CLI interface**: Correct flag handling and output formatting
6. **GUI interface**: Dynamic field updates and error display
7. **Error display**: Proper error message presentation
8. **Extensibility**: New converters work seamlessly
9. **DMS round-trip**: DMS format conversions preserve precision

## Precision and Tolerance

- **Geographic**: 6 decimal places (~0.11 meters), round-trip tolerance 0.000001 degrees
- **MGRS**: 1 meter precision, round-trip tolerance 1 meter
- **USK-2000**: 2 decimal places (centimeters), round-trip tolerance 1 meter

## Error Handling

The application provides clear error messages for:
- Invalid coordinate values (out of bounds)
- Malformed input strings
- Unsupported coordinate systems
- Conversion failures

## Future Enhancements

Potential additions:
- UTM (Universal Transverse Mercator)
- Gauss-Krüger coordinates
- Batch conversion from files
- Auto-format detection
- Precision control
- Export to CSV/JSON/KML
- Map visualization

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please ensure:
- All tests pass (`pytest`)
- Code follows the existing style
- New features include tests
- Documentation is updated

## Support

For issues, questions, or suggestions, please open an issue on the project repository.

## Acknowledgments

- [mgrs](https://github.com/asfadmin/mgrs) - MGRS coordinate library
- [pyproj](https://github.com/pyproj4/pyproj) - Coordinate transformation library
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) - Modern Tkinter themes
