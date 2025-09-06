#!/usr/bin/env python3
# main.py
import sys
import traceback
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import your main window class
from main_window import MainWindow

def main():
    try:
        # Create QApplication instance
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName("2004Scape Toolkit")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("2004Scape")
        
        # Try to load and set the RuneScape font
        try:
            font = QFont("RuneScape UF")
            if not font.exactMatch():
                font = QFont("runescape_uf")
            app.setFont(font)
        except Exception as font_error:
            print(f"Warning: Could not load RuneScape font: {font_error}")
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        # Start the application event loop
        sys.exit(app.exec())
        
    except ImportError as e:
        error_msg = f"Import Error: {e}\n\nMissing required modules. Please install:\npip install PyQt6 PyQt6-WebEngine"
        print(error_msg)
        try:
            app = QApplication(sys.argv)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Import Error")
            msg.setText(error_msg)
            msg.exec()
        except:
            pass
    except Exception as e:
        error_msg = f"Unexpected error: {e}\n\nFull traceback:\n{traceback.format_exc()}"
        print(error_msg)
        try:
            app = QApplication(sys.argv)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Application Error")
            msg.setText(str(e))
            msg.setDetailedText(traceback.format_exc())
            msg.exec()
        except:
            pass

if __name__ == "__main__":
    main()