from utils.globals import initialize_database
from gui.main_window import MainWindow
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Apliación de escritorio para la gestión de libros."
    )
    parser.add_argument(
        "--user",
        help="El nombre del usuario con el que se desea iniciar sesión.",
        required=True,
    )
    parser.add_argument(
        "--no-gui",
        help="Ejecutar la aplicación en modo consola.",
        action="store_true",
    )

    args = parser.parse_args()

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