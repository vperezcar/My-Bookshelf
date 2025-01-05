from utils.globals import initialize_database
from gui.main_window import MainWindow
import sys
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="My Bookshelf: An application to manage your books."
    )
    parser.add_argument(
        "--user",
        help="(Optional) The name of the user to log in with.",
    )
    parser.add_argument(
        "--no-gui",
        help="Run the application in console mode.",
        action="store_true",
    )

    args = parser.parse_args()

    if not args.user:
        args.user = os.getenv("USER")

    # Initialize database creating its tables and adding the user if not exists
    initialize_database(args.user)
    if args.no_gui:
        from no_gui.no_gui import no_gui_app

        no_gui_app()
    else:
        from PyQt6 import QtWidgets

        app = QtWidgets.QApplication(sys.argv)
        MainWindow().show()
        sys.exit(app.exec())
