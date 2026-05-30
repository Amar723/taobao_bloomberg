import sys
from commands.ovdv.app import app
from commands.ovdv.fetch import get_vol_surface
from commands.ovdv.surface import build_surface

command = sys.argv[1] if len(sys.argv) > 1 else None
ticker  = sys.argv[2] if len(sys.argv) > 2 else "SPY"

if command == "OVDV":
    app.run(debug=True)