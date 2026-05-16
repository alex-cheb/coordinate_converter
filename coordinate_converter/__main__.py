"""Main entry point for the Coordinate Converter application."""

import sys
import argparse

def main():
    """Main entry point to route to CLI or GUI based on arguments."""
    parser = argparse.ArgumentParser(
        prog="coordinate_converter",
        description="Coordinate Converter - Convert between differend coordinate systems"
        )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the GUI interface. Default if no coordinates provided."
        )
        
    args, remaining = parser.parse_known_args()
    
    if args.gui:
        from .interfaces.gui import CoordinateConverterGUI
        app = CoordinateConverterGUI()
        app.mainloop()
    else:
        from .interfaces.cli import main as cli_main
        cli_main()
        
if __name__ == "__main__":
    main()