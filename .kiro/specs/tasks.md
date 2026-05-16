# Implementation Plan: Coordinate Converter

## Overview

This implementation plan breaks down the Coordinate Converter feature into discrete coding tasks. The system uses a functional approach for business logic (conversion engine and converters) and a class-based approach for the GUI. The implementation follows a bottom-up strategy: core data models → conversion engine → converters → interfaces → testing.

## Tasks

- [x] 1. Set up project structure and core data models
  - Create directory structure: `coordinate_converter/`, `core/`, `converters/`, `interfaces/`, `tests/`
  - Create all `__init__.py` files for Python packages
  - Implement data models in `core/models.py`: `GeographicCoordinates`, `ConversionResult`, `ValidationResult`, `CLIArguments` as frozen dataclasses
  - Add `to_dms()` method to `GeographicCoordinates` for DMS format conversion
  - _Requirements: 3.1, 3.2, 7.2_

- [x] 2. Implement conversion engine core
  - [x] 2.1 Create conversion engine in `core/engine.py`
    - Implement `_converter_registry` dictionary for storing converter modules
    - Implement `register_converter(system_name, converter_module)` function
    - Implement `get_supported_systems()` function to return list of registered systems
    - Define `ConverterModule` Protocol with required function signatures
    - _Requirements: 3.1, 3.2, 6.1_

  - [x] 2.2 Implement core conversion logic
    - Implement `convert(input_system, coordinates)` function
    - Add validation that input system exists in registry
    - Add logic to convert input → geographic → all other systems
    - Return `ConversionResult` with success/error information
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 3.3_

- [x] 3. Implement geographic coordinate converter
  - [x] 3.1 Create geographic converter module in `converters/geographic.py`
    - Implement `detect_format(input_string)` to distinguish decimal vs DMS format
    - Implement `parse_decimal(input_string)` to parse "49.0000, 37.0000" format
    - Implement `parse_dms(input_string)` to parse "49°00'00.1"N 37°00'00.1"E" format
    - Implement `dms_to_decimal(dms_string)` helper function
    - Implement `decimal_to_dms(latitude, longitude)` to format as DMS string
    - _Requirements: 1.1, 7.2, 7.3_

  - [x] 3.2 Implement geographic converter interface functions
    - Implement `validate(coordinates)` to check latitude [-90, 90] and longitude [-180, 180]
    - Implement `to_geographic(coordinates)` as identity transformation
    - Implement `from_geographic(geo_coords)` as identity transformation
    - Implement `format_output(coordinates)` to show both decimal and DMS formats
    - _Requirements: 1.1, 2.1, 8.1, 8.2, 8.3_

  - [ ]* 3.3 Write property test for geographic converter
    - **Property 9: DMS format round-trip preserves coordinates**
    - **Validates: Requirements 7.1, 7.2**
    - Generate random valid decimal coordinates, convert to DMS, parse back to decimal, assert within tolerance

  - [ ]* 3.4 Write unit tests for geographic converter
    - Test `detect_format()` with decimal and DMS inputs
    - Test `parse_decimal()` with various valid formats (comma/space separated)
    - Test `parse_dms()` with various valid DMS formats
    - Test `decimal_to_dms()` with known conversions
    - Test edge cases: 0°, 90°N, 180°E, negative coordinates
    - Test invalid inputs: out of bounds, malformed strings
    - _Requirements: 2.1, 7.1, 7.2_

- [x] 4. Implement MGRS converter
  - [x] 4.1 Create MGRS converter module in `converters/mgrs.py`
    - Implement `validate(coordinates)` to check MGRS string format
    - Implement `to_geographic(coordinates)` using mgrs library
    - Implement `from_geographic(geo_coords)` using mgrs library
    - Implement `format_output(coordinates)` for standard MGRS string format
    - Add error handling for mgrs library exceptions
    - _Requirements: 1.2, 2.2, 8.1, 8.2, 8.3_

  - [ ]* 4.2 Write property test for MGRS converter
    - **Property 1: Round-trip conversion preserves coordinates (MGRS)**
    - **Validates: Requirements 7.1**
    - Generate random valid MGRS coordinates, convert to geographic and back, assert within 1 meter tolerance

  - [ ]* 4.3 Write unit tests for MGRS converter
    - Test known MGRS coordinate conversions
    - Test edge cases: grid zone boundaries, polar regions
    - Test invalid MGRS strings
    - Test precision maintenance
    - _Requirements: 1.2, 2.2, 7.1_

- [x] 5. Implement USK-2000 converter
  - [x] 5.1 Create USK-2000 converter module in `converters/usk2000.py`
    - Implement `validate(coordinates)` to check USK-2000 coordinate bounds
    - Implement `to_geographic(coordinates)` using pyproj with EPSG:5561
    - Implement `from_geographic(geo_coords)` using pyproj with EPSG:5561
    - Implement `format_output(coordinates)` for USK-2000 conventions (2 decimal places)
    - Add error handling for pyproj exceptions
    - _Requirements: 1.3, 2.3, 8.1, 8.2, 8.3_

  - [ ]* 5.2 Write property test for USK-2000 converter
    - **Property 1: Round-trip conversion preserves coordinates (USK-2000)**
    - **Validates: Requirements 7.1**
    - Generate random valid USK-2000 coordinates, convert to geographic and back, assert within 1 meter tolerance

  - [ ]* 5.3 Write unit tests for USK-2000 converter
    - Test known USK-2000 coordinate conversions (e.g., Kyiv city center)
    - Test coordinates at Ukraine boundaries
    - Test invalid coordinates (outside Ukraine bounds)
    - Test precision maintenance (2 decimal places)
    - _Requirements: 1.3, 2.3, 7.1, 7.2_

- [ ] 6. Checkpoint - Ensure all converter tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Wire converters to conversion engine
  - [x] 7.1 Create initialization module
    - Import all converter modules (geographic, mgrs, usk2000)
    - Register each converter with the conversion engine using `register_converter()`
    - Create initialization function to set up registry at startup
    - _Requirements: 3.1, 3.4, 6.1, 6.2_

  - [ ]* 7.2 Write property test for conversion engine
    - **Property 2: Conversion completeness and validity**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 8.4**
    - Generate random valid coordinates in each system, convert, verify all other systems present with valid coordinates

  - [ ]* 7.3 Write property test for error handling
    - **Property 3: Invalid input error handling**
    - **Validates: Requirements 2.1, 2.2, 2.3**
    - Generate invalid coordinates in each system, verify descriptive error messages returned

  - [ ]* 7.4 Write property test for output format
    - **Property 4: Output format correctness**
    - **Validates: Requirements 7.2, 7.3, 8.1, 8.2, 8.3**
    - Generate random valid coordinates, verify plain text output with labels and correct precision

  - [ ]* 7.5 Write unit tests for conversion engine
    - Test `register_converter()` adds converters to registry
    - Test `get_supported_systems()` returns correct list
    - Test `convert()` with unsupported system returns error
    - Test `convert()` orchestrates conversions correctly
    - _Requirements: 3.1, 3.2, 3.3, 6.2_

- [ ] 8. Implement CLI interface
  - [x] 8.1 Create CLI module in `interfaces/cli.py`
    - Implement `parse_arguments(args)` using argparse
    - Add `-g` flag for geographic input (supports both decimal and DMS)
    - Add `-m` flag for MGRS input
    - Add `-u` flag for USK-2000 input
    - Add validation that exactly one flag is provided
    - Return `CLIArguments` dataclass
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 8.2 Implement CLI execution logic
    - Implement `execute(args)` function to invoke conversion engine
    - Format output as plain text with system labels
    - Handle errors by printing to stderr and exiting with non-zero status
    - Implement `main()` entry point
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.6_

  - [ ]* 8.3 Write property test for CLI interface
    - **Property 5: CLI interface conversion correctness**
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.6**
    - Generate random valid coordinates, invoke CLI with appropriate flags, verify plain text output

  - [ ]* 8.4 Write unit tests for CLI
    - Test `parse_arguments()` with each flag type
    - Test with no arguments (should show usage)
    - Test with multiple flags (should error)
    - Test with unsupported flag (should error)
    - Test `-g` flag with decimal format
    - Test `-g` flag with DMS format (quoted string)
    - Test end-to-end CLI execution for each coordinate system
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 9. Implement GUI interface
  - [x] 9.1 Create GUI module in `interfaces/gui.py`
    - Create `CoordinateConverterGUI` class with `__init__` method
    - Initialize Tkinter root window with ttkbootstrap theme
    - Create instance variables: `selected_system`, `selected_geo_type`, `input_fields`
    - _Requirements: 5.1, 5.7_

  - [x] 9.2 Implement GUI layout and input system selector
    - Implement `_create_widgets()` method to create widget layout
    - Add dropdown for input system selection (Geographic, MGRS, USK2000)
    - Add geographic format mode selector (Decimal vs DMS radio buttons)
    - Implement `_on_system_change()` handler to update input fields dynamically
    - Implement `_on_geo_coord_type_change()` handler to switch between decimal/DMS input
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 9.3 Implement dynamic input fields
    - Create input fields for Geographic Decimal mode (two fields: Latitude, Longitude)
    - Create input field for Geographic DMS mode (single field with format example)
    - Create input field for MGRS (single field)
    - Create input fields for USK-2000 (X and Y fields)
    - Add format hints/placeholder text for DMS and MGRS input
    - _Requirements: 5.2, 5.3, 5.4_

  - [x] 9.4 Implement conversion and output display
    - Add Convert button with click handler
    - Implement `_on_convert()` method to invoke conversion engine
    - Implement `_display_result(result)` method to show all converted systems
    - Ensure geographic output shows both decimal and DMS formats
    - _Requirements: 5.5, 8.1, 8.2_

  - [x] 9.5 Implement error handling and display
    - Display errors in output text area
    - Clear error messages before new conversion attempts
    - Disable convert button when no system selected and during conversion to prevent double-clicks
    - _Requirements: 5.6_

  - [ ]* 9.6 Write property test for GUI conversion
    - **Property 6: GUI conversion correctness**
    - **Validates: Requirements 5.5**
    - Generate random valid coordinates, simulate GUI conversion, verify output display

  - [ ]* 9.7 Write property test for GUI error display
    - **Property 7: GUI error display**
    - **Validates: Requirements 5.6**
    - Generate invalid coordinates, simulate GUI conversion, verify error display

  - [ ]* 9.8 Write unit tests for GUI
    - Test input field visibility changes when system selected
    - Test geographic format mode switching (decimal <-> DMS)
    - Test button click handlers
    - Test output area updates (should show both decimal and DMS)
    - Test error display functionality
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [X] 9.9 Show alternate geographic format in output
    - When decimal geographic input is provided, show DMS format in output
    - When DMS geographic input is provided, show decimal format in output
    - Update `_display_result()` to include both formats for geographic system
    - Ensure the alternate format appears in the formatted output alongside other conversions
    - _Requirements: 7.2, 8.1_

  - [X] 9.10 Customize output text styling
    - Configure output text widget font size for better readability
    - Apply color styling to output text (success vs error states)
    - Apply font styling (bold for labels, regular for values)
    - Use Tkinter Text widget tags for styling different parts of output
    - Ensure styling is consistent with ttkbootstrap theme
    - _Requirements: 5.5, 5.7_

- [ ] 10. Checkpoint - Ensure all interface tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement extensibility property test
  - [ ]* 11.1 Write property test for extensibility
    - **Property 8: Extensibility through registration**
    - **Validates: Requirements 6.2**
    - Create mock converter module, register with engine, verify it's used in conversions and appears in supported systems list

- [ ] 12. Create main entry points and package configuration
  - [ ] 12.1 Create main entry points
    - Create `__main__.py` for CLI entry point
    - Create launcher script for GUI
    - Add command-line argument to choose interface (CLI vs GUI)
    - _Requirements: 4.1, 5.1_

  - [ ] 12.2 Create package configuration
    - Create `setup.py` or `pyproject.toml` for package installation
    - Specify dependencies: mgrs>=1.4.0, pyproj>=3.4.0, ttkbootstrap>=1.10.0
    - Specify dev dependencies: pytest>=7.0.0, hypothesis>=6.0.0, pytest-cov>=4.0.0
    - Add console script entry points for CLI and GUI
    - _Requirements: 3.1_

  - [ ]* 12.3 Write integration tests
    - Test end-to-end CLI conversion for each supported system
    - Test end-to-end GUI conversion for each supported system
    - Test adding a new coordinate system and verifying it works in both interfaces
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 6.2_

- [ ] 13. Final checkpoint - Ensure all tests pass
  - Run complete test suite with pytest
  - Verify all property-based tests pass (minimum 100 iterations each)
  - Verify test coverage meets goals (100% core logic, 90%+ interfaces)
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests use Hypothesis library with minimum 100 iterations
- Each property test is tagged with comment: `# Feature: coordinate-converter, Property {number}: {property_text}`
- Checkpoints ensure incremental validation
- The implementation follows a bottom-up approach: data models → engine → converters → interfaces
- Geographic coordinates support both decimal and DMS input/output formats
- GUI uses class-based approach for state management; business logic uses functional approach
- All converters use geographic coordinates (WGS84) as intermediate format
