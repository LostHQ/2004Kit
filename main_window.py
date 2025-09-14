# main_window.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QSplitter, 
                             QVBoxLayout, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from game_view import GameViewWidget
from right_panel import RightToolsPanel, InGameBrowser
import config
from styles import MAIN_STYLESHEET
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2004Kit")
        
        # Set window icon if it exists
        if os.path.exists("icon.ico"):
            self.setWindowIcon(QIcon("icon.ico"))
        
        # Force RuneScape font
        font = QFont("RuneScape UF")
        if not font.exactMatch():
            font = QFont("runescape_uf")
        self.setFont(font)
        
        # Load config
        self.config = config.load_config()
        
        # Set window geometry from config or default
        try:
            if self.config.get("window_geometry"):
                geom = self.config["window_geometry"]
                if isinstance(geom, list) and len(geom) == 4:
                    # Ensure all values are integers
                    x, y, w, h = [int(val) for val in geom]
                    self.setGeometry(x, y, w, h)
                else:
                    self.setGeometry(100, 100, 1280, 720)
            else:
                self.setGeometry(100, 100, 1280, 720)
        except (ValueError, TypeError) as e:
            print(f"Error setting window geometry: {e}, using defaults")
            self.setGeometry(100, 100, 1280, 720)
        
        # Apply stylesheet
        self.setStyleSheet(MAIN_STYLESHEET)
        
        # Set minimum size
        self.setMinimumSize(800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create main splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side: Game view with optional browser tabs
        self.left_widget = QWidget()
        left_layout = QVBoxLayout(self.left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget for game and tools
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_browser_tab)
        
        # Game view tab (always present)
        self.game_view = GameViewWidget("https://2004.lostcity.rs/serverlist?lores.x=55&lores.y=62&method=0")
        self.game_view.setZoomFactor(self.config.get("zoom_factor", 1.0))
        self.tab_widget.addTab(self.game_view, "⚔️ LostCity")
        
        # Make game tab unclosable
        self.tab_widget.tabBar().setTabButton(0, self.tab_widget.tabBar().ButtonPosition.RightSide, None)
        
        left_layout.addWidget(self.tab_widget)
        self.splitter.addWidget(self.left_widget)

        # Right side: Tools panel
        self.tools_panel = RightToolsPanel()
        self.tools_panel.browser_requested.connect(self.open_browser_tab)
        self.splitter.addWidget(self.tools_panel)

        # Set initial splitter sizes
        panel_width = self.config.get("right_panel_width", 250)
        total_width = self.width()
        game_width = total_width - panel_width
        self.splitter.setSizes([game_width, panel_width])
        
        # Connect splitter moved signal to save config
        self.splitter.splitterMoved.connect(self.on_splitter_moved)

        layout.addWidget(self.splitter)
        self.setCentralWidget(central_widget)
        
        # Track browser tabs
        self.browser_tabs = {}

    def open_browser_tab(self, url, title):
        """Open a tool in a new tab within the main window"""
        print(f"Opening browser tab: {title} - {url}")  # Debug print
        
        # Get icon for this tool
        from styles import get_icon_path
        icon = get_icon_path(title)
        tab_title = f"{icon} {title}"
        
        # Check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == tab_title:
                self.tab_widget.setCurrentIndex(i)
                return
        
        try:
            # Create new browser tab
            browser = InGameBrowser(url, title)
            browser.closed.connect(lambda: self.close_browser_by_widget(browser))
            
            # Add tab with proper icon
            tab_index = self.tab_widget.addTab(browser, tab_title)
            self.tab_widget.setCurrentIndex(tab_index)
            
            # Store reference
            self.browser_tabs[tab_index] = browser
            
        except Exception as e:
            print(f"Error creating browser tab: {e}")

    def close_browser_tab(self, index):
        """Close a browser tab"""
        if index == 0:  # Can't close game tab
            return
            
        widget = self.tab_widget.widget(index)
        if widget:
            # Remove from tracking
            if index in self.browser_tabs:
                del self.browser_tabs[index]
            
            # Remove tab
            self.tab_widget.removeTab(index)
            widget.deleteLater()

    def close_browser_by_widget(self, browser_widget):
        """Close browser tab by widget reference"""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.widget(i) == browser_widget:
                self.close_browser_tab(i)
                break

    def on_splitter_moved(self, pos, index):
        """Save splitter position to config"""
        sizes = self.splitter.sizes()
        if len(sizes) >= 2:
            self.config["right_panel_width"] = sizes[1]
            config.save_config(self.config)

    def closeEvent(self, event):
        """Save window state when closing"""
        # Save window geometry
        geom = self.geometry()
        self.config["window_geometry"] = [geom.x(), geom.y(), geom.width(), geom.height()]
        
        # Save zoom factor
        self.config["zoom_factor"] = self.game_view.zoom_factor
        
        # Save splitter sizes
        sizes = self.splitter.sizes()
        if len(sizes) >= 2:
            self.config["right_panel_width"] = sizes[1]
        
        config.save_config(self.config)
        event.accept()

    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        # Maintain right panel width ratio
        if hasattr(self, 'splitter'):
            panel_width = self.config.get("right_panel_width", 250)
            total_width = self.width()
            game_width = max(400, total_width - panel_width)  # Minimum game width
            self.splitter.setSizes([game_width, panel_width])

    def setup_window_style(self):
        """Setup custom window styling including title bar"""
        try:
            # Try to set custom title bar color on Windows
            if sys.platform == "win32":
                import ctypes
                from ctypes import wintypes
                
                # Get window handle
                hwnd = int(self.winId())
                
                # Define constants for Windows API
                DWMWA_CAPTION_COLOR = 35
                DWMWA_BORDER_COLOR = 34
                
                # Convert color to Windows format (BGR)
                # Dark pastel brown: #4a3428 -> 0x28344a
                color = 0x28344a
                
                try:
                    # Try to load dwmapi.dll
                    dwmapi = ctypes.windll.dwmapi
                    
                    # Set caption color
                    dwmapi.DwmSetWindowAttribute(
                        wintypes.HWND(hwnd),
                        wintypes.DWORD(DWMWA_CAPTION_COLOR),
                        ctypes.byref(wintypes.DWORD(color)),
                        ctypes.sizeof(wintypes.DWORD)
                    )
                    
                    # Set border color
                    dwmapi.DwmSetWindowAttribute(
                        wintypes.HWND(hwnd),
                        wintypes.DWORD(DWMWA_BORDER_COLOR),
                        ctypes.byref(wintypes.DWORD(color)),
                        ctypes.sizeof(wintypes.DWORD)
                    )
                    
                    print("✅ Custom title bar color applied")
                    
                except Exception as e:
                    print(f"⚠️  Could not set custom title bar color: {e}")
                    
        except ImportError:
            # Not on Windows or missing modules
            pass
        except Exception as e:

            print(f"Warning: Could not apply window styling: {e}")
