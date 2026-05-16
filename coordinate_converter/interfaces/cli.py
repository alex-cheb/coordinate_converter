import argparse
import coordinate_converter
from ..core.models import CLIArguments



def parse_arguments(arg):
    """Parse command-line arguments for the Coordinate Converter CLI."""
    parser = argparse.ArgumentParser(
        prog="coordinate_converter",
        description="Coordinate Converter CLI",
        epilog="Example usage: coordinate_converter -g 40.7128 -74.0060. Supported arguments: -g for geographic; -u for USK-2000, -m for MGRS, -h for help.",
    )

    # Create mutually exclusive group - ensures only ONE flag is used
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--geographic", nargs=2, metavar=('LAT', 'LON'), type=float, help="Input is provided as Geographic coordinates (latitude longitude)")
    group.add_argument("-u", "--usk2000", nargs=2, metavar=('X', 'Y'), type=float, help="Input is provided as USK-2000 coordinates")
    group.add_argument("-m", "--mgrs", help="Input is provided as MGRS coordinates")
    
    parsed = parser.parse_args(arg)
    
    return CLIArguments(input_system=_get_input_system(parsed), coordinates=_get_coordinates(parsed))

def execute(args):
    """Execute the coordinate conversion based on the parsed CLI arguments."""
    from ..core.engine import convert

    result = convert(args.input_system, args.coordinates)

    if result.success:
        for system, formatted_output in result.conversions.items():
            print(formatted_output)

    else:
        import sys
        print(f"Error: {result.error_msg}", file=sys.stderr)
        sys.exit(1)

def _get_input_system(parsed):
    """Determine which input system was specified based on the parsed arguments."""
    if parsed.geographic:
        return "geographic"
    elif parsed.usk2000:
        return "usk2000"
    elif parsed.mgrs:
        return "mgrs"
    else:
        raise ValueError("No valid input system found in arguments.")
    
    
def _get_coordinates(parsed):
    """Extract coordinates based on the parsed arguments."""
    if parsed.geographic:
        return {"latitude": parsed.geographic[0], "longitude": parsed.geographic[1]}
    elif parsed.usk2000:
        return {"x":parsed.usk2000[0], "y": parsed.usk2000[1]}
    elif parsed.mgrs:
        return {"mgrs_string": parsed.mgrs}
    else:
        raise ValueError("No valid coordinates found in arguments.")
    

def main():
    """Main entry point for the Coordinate Converter CLI."""
    import sys
    args = parse_arguments(sys.argv[1:])
    execute(args)

if __name__ == "__main__":
    main()