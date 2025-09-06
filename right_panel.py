# right_panel.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QGroupBox, 
                             QCheckBox, QScrollArea, QHBoxLayout, QLabel)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtCore import QUrl, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
from config import load_config, save_config, get_config_value, set_config_value
from styles import get_icon_path
import os


class ToolWindow(QWidget):
    def __init__(self, url, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"2004Kit - {title}")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)  # Ensure proper cleanup
        
        # Set window icon if it exists
        if os.path.exists("icon.ico"):
            self.setWindowIcon(QIcon("icon.ico"))
        
        # Force RuneScape font
        font = QFont("RuneScape UF")
        if not font.exactMatch():
            font = QFont("runescape_uf")
        self.setFont(font)
        
        # Load window geometry from config with error handling
        try:
            geom = get_config_value("tool_window_geometry", [200, 200, 900, 700])
            if isinstance(geom, list) and len(geom) == 4:
                x, y, w, h = [int(val) for val in geom]
                self.setGeometry(x, y, w, h)
            else:
                self.setGeometry(200, 200, 900, 700)
        except (ValueError, TypeError) as e:
            print(f"Error setting tool window geometry: {e}, using defaults")
            self.setGeometry(200, 200, 900, 700)
        
        # Make window resizable
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Use separate profile for each window to avoid conflicts
        profile_name = f"ToolWindow_{title.replace(' ', '_')}"
        profile = QWebEngineProfile(profile_name, self)
        profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )

        page = QWebEnginePage(profile, self)
        self.web_view = QWebEngineView()
        self.web_view.setPage(page)
        
        layout.addWidget(self.web_view)
        
        # Load URL after everything is set up
        print(f"Loading URL in window: {url}")
        self.web_view.setUrl(QUrl(url))

    def closeEvent(self, event):
        # Save window geometry when closing
        try:
            geom = self.geometry()
            set_config_value("tool_window_geometry", [geom.x(), geom.y(), geom.width(), geom.height()])
        except Exception as e:
            print(f"Error saving window geometry: {e}")
        event.accept()


class InGameBrowser(QWidget):
    """Browser widget that can be embedded in the main window"""
    closed = pyqtSignal()
    
    def __init__(self, url, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.url = url
        self.title = title
        
        # Force RuneScape font
        font = QFont("RuneScape UF")
        if not font.exactMatch():
            font = QFont("runescape_uf")
        self.setFont(font)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins since tab already handles close

        # Web view only - no title bar or close button since tab handles that
        profile = QWebEngineProfile.defaultProfile()
        page = QWebEnginePage(profile, self)
        view = QWebEngineView()
        view.setPage(page)
        view.setUrl(QUrl(url))

        layout.addWidget(view)
        
        # Store reference to view for potential future use
        self.web_view = view

    def close_browser(self):
        """Close the browser tab - this method was missing!"""
        try:
            # Stop the web view if it exists
            if hasattr(self, 'web_view') and self.web_view:
                self.web_view.stop()
                self.web_view.setParent(None)
            
            # Emit the closed signal so parent can handle cleanup
            self.closed.emit()
            
            # Close/hide this widget
            self.close()
            
        except Exception as e:
            print(f"Error closing browser: {e}")


class RightToolsPanel(QWidget):
    browser_requested = pyqtSignal(str, str)  # url, title
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.tool_buttons = []
        self.open_windows = []  # Keep references to open windows to prevent garbage collection
        
        # Force RuneScape font
        font = QFont("RuneScape UF")
        if not font.exactMatch():
            font = QFont("runescape_uf")
        self.setFont(font)

        # Create main layout with no spacing at bottom
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Settings Group
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()
        
        self.external_checkbox = QCheckBox("Open tools in separate windows")
        self.external_checkbox.setChecked(self.config.get("open_external", True))
        self.external_checkbox.stateChanged.connect(self.on_external_changed)
        
        settings_layout.addWidget(self.external_checkbox)
        settings_group.setLayout(settings_layout)
        
        # Set fixed height for settings group to prevent it from expanding
        settings_group.setFixedHeight(80)
        main_layout.addWidget(settings_group)

        # Tools Group - this should take up remaining space
        tools_group = QGroupBox("Tools")
        tools_layout = QVBoxLayout()
        tools_layout.setContentsMargins(5, 10, 5, 5)
        
        # Scroll area for tools - this will expand to fill available space
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Remove any size constraints that might limit the scroll area
        scroll_area.setMinimumHeight(0)
        scroll_area.setSizePolicy(scroll_area.sizePolicy().Policy.Expanding, 
                                 scroll_area.sizePolicy().Policy.Expanding)
        
        scroll_widget = QWidget()
        self.tools_layout = QVBoxLayout(scroll_widget)
        self.tools_layout.setSpacing(5)
        self.tools_layout.setContentsMargins(5, 5, 5, 5)
        
        # Define tools list - Updated with new tools
        self.tools_data = [
            ("Forums", "https://lostcity.rs"),
            ("Clue Coordinates", "https://razgals.github.io/2004-Coordinates/"),
            ("Clue Scroll Help", "https://razgals.github.io/Treasure/"),
            ("World Map", "https://2004.lostcity.rs/worldmap"),
            ("Highscores", "https://2004.lostcity.rs/hiscores"),
            ("Market Prices", "https://lostcity.markets"),
            ("Quest Help", "https://2004.losthq.rs/?p=questguides"),
            ("Skill Guides", "https://2004.losthq.rs/?p=skillguides"),
            ("Skills Calculator", "https://2004.losthq.rs/?p=calculators"),
            ("Bestiary", "https://2004.losthq.rs/?p=droptables"),
        ]

        # Create tool buttons
        self.setup_tool_buttons()
        
        scroll_area.setWidget(scroll_widget)
        tools_layout.addWidget(scroll_area)
        tools_group.setLayout(tools_layout)
        
        # Add tools group with stretch factor so it expands to fill remaining space
        main_layout.addWidget(tools_group, 1)  # stretch factor of 1

    def setup_tool_buttons(self):
        """Create all tool buttons"""
        # Clear existing buttons
        for button in self.tool_buttons:
            button.setParent(None)
            button.deleteLater()
        self.tool_buttons.clear()

        # Create buttons for each tool
        for i, (name, url) in enumerate(self.tools_data):
            btn = QPushButton()
            
            # Force RuneScape font on button
            font = QFont("RuneScape UF")
            if not font.exactMatch():
                font = QFont("runescape_uf")
            btn.setFont(font)
            
            # Set button background image if button.jpg exists
            if os.path.exists("button.jpg"):
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-image: url(button.jpg);
                        border: 2px solid #2a2a2a;
                        border-radius: 8px;
                        padding: 8px;
                        color: #f5e6c0;
                        font-weight: bold;
                        min-height: 40px;
                        text-align: left;
                    }}
                    QPushButton:hover {{
                        border-color: #8b4a4a;
                        background-color: rgba(139, 74, 74, 0.3);
                    }}
                    QPushButton:pressed {{
                        border: 2px inset #2a2a2a;
                        background-color: rgba(139, 74, 74, 0.5);
                    }}
                """)
            
            # Set button text with icon and name
            icon = get_icon_path(name)
            btn.setText(f"{icon}  {name}")
            btn.setToolTip(name)
            
            # Set button size
            btn.setMinimumHeight(50)
            btn.setMaximumHeight(60)
            
            # Set size policy to expand horizontally but keep fixed height
            btn.setSizePolicy(btn.sizePolicy().Policy.Expanding, 
                             btn.sizePolicy().Policy.Fixed)
            
            # Connect button click - using partial to avoid lambda closure issue
            def make_click_handler(tool_url, tool_name):
                return lambda: self.open_tool_clicked(tool_url, tool_name)
            
            btn.clicked.connect(make_click_handler(url, name))
            
            # Add to layout and track
            self.tools_layout.addWidget(btn)
            self.tool_buttons.append(btn)
            
        # Add stretch at the bottom to push buttons to top if there's extra space
        self.tools_layout.addStretch()

    def on_external_changed(self, state):
        """Handle external window checkbox change"""
        is_external = state == Qt.CheckState.Checked.value
        self.config["open_external"] = is_external
        save_config(self.config)

    def open_tool_clicked(self, url, title):
        """Handle tool button click"""
        print(f"Opening tool: {title} - {url}")  # Debug print
        if self.config.get("open_external", True):
            # Open in separate window
            try:
                # Check if window already exists
                for window in self.open_windows[:]:  # Use slice to avoid modification during iteration
                    if not window.isVisible():  # Remove closed windows
                        self.open_windows.remove(window)
                    elif window.windowTitle() == f"2004Kit - {title}":
                        # Window already exists, bring it to front
                        window.show()
                        window.activateWindow()
                        window.raise_()
                        return
                
                # Create new window - no parent reference to make it truly independent
                window = ToolWindow(url, title, None)
                
                # Connect window destroyed signal to remove from list
                window.destroyed.connect(lambda: self.remove_window_from_list(window))
                
                # Add to list to keep reference
                self.open_windows.append(window)
                
                # Show window
                window.show()
                window.activateWindow()
                window.raise_()
                
                print(f"✅ Successfully opened window: {title}")
                
            except Exception as e:
                print(f"❌ Error opening tool window: {e}")
                import traceback
                traceback.print_exc()
        else:
            # Open in main window tab
            try:
                self.browser_requested.emit(url, title)
            except Exception as e:
                print(f"Error opening browser tab: {e}")

    def remove_window_from_list(self, window):
        """Remove window from list when it's destroyed"""
        try:
            if window in self.open_windows:
                self.open_windows.remove(window)
        except:
            pass  # Window might already be removed