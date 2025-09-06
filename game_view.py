# game_view.py
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtCore import Qt, QUrl, QDir, pyqtSignal
import config


class GameViewWidget(QWebEngineView):
    zoom_changed = pyqtSignal(float)
    
    def __init__(self, url, parent=None):
        super().__init__(parent)

        try:
            # Setup persistent profile
            profile = QWebEngineProfile("2004Client", self)
            profile.setCachePath(QDir.currentPath() + "/web_cache")
            profile.setPersistentStoragePath(QDir.currentPath() + "/web_storage")
            
            # Enable developer tools for debugging if needed
            # profile.settings().setAttribute(
            #     QWebEngineProfile.WebEngineSettings.WebAttribute.DeveloperExtrasEnabled, True
            # )

            page = QWebEnginePage(profile, self)
            self.setPage(page)

            # Load the game
            self.setUrl(QUrl(url))

            # Load zoom factor from config
            self.zoom_factor = config.get_config_value("zoom_factor", 1.0)
            self.setZoomFactor(self.zoom_factor)

            # Connect signals
            self.page().loadFinished.connect(self.on_load_finished)
            
            # Enable focus for keyboard events
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            
        except Exception as e:
            print(f"Error initializing GameViewWidget: {e}")
            # Set a basic zoom factor as fallback
            self.zoom_factor = 1.0

    def on_load_finished(self, ok: bool):
        """Handle page load completion"""
        if ok:
            print("✅ Game page loaded successfully.")
            # Apply saved zoom factor after page loads
            try:
                self.setZoomFactor(self.zoom_factor)
            except Exception as e:
                print(f"Error setting zoom factor: {e}")
        else:
            print("❌ Failed to load game page.")

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming"""
        try:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                # Ctrl + wheel = zoom
                delta = event.angleDelta().y()
                zoom_step = 0.1
                
                if delta > 0:
                    self.zoom_factor += zoom_step
                else:
                    self.zoom_factor -= zoom_step
                    
                # Clamp zoom factor to reasonable bounds
                self.zoom_factor = max(0.25, min(self.zoom_factor, 5.0))
                
                # Apply zoom
                self.setZoomFactor(self.zoom_factor)
                
                # Save to config
                config.set_config_value("zoom_factor", self.zoom_factor)
                
                # Emit signal
                self.zoom_changed.emit(self.zoom_factor)
                
                # Accept event to prevent scrolling
                event.accept()
            else:
                # Normal scrolling
                super().wheelEvent(event)
        except Exception as e:
            print(f"Error in wheelEvent: {e}")
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        try:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                if event.key() == Qt.Key.Key_0:
                    # Ctrl+0: Reset zoom to 100%
                    self.zoom_factor = 1.0
                    self.setZoomFactor(self.zoom_factor)
                    config.set_config_value("zoom_factor", self.zoom_factor)
                    self.zoom_changed.emit(self.zoom_factor)
                    event.accept()
                    return
                elif event.key() == Qt.Key.Key_Plus or event.key() == Qt.Key.Key_Equal:
                    # Ctrl++: Zoom in
                    self.zoom_factor = min(self.zoom_factor + 0.1, 5.0)
                    self.setZoomFactor(self.zoom_factor)
                    config.set_config_value("zoom_factor", self.zoom_factor)
                    self.zoom_changed.emit(self.zoom_factor)
                    event.accept()
                    return
                elif event.key() == Qt.Key.Key_Minus:
                    # Ctrl+-: Zoom out
                    self.zoom_factor = max(self.zoom_factor - 0.1, 0.25)
                    self.setZoomFactor(self.zoom_factor)
                    config.set_config_value("zoom_factor", self.zoom_factor)
                    self.zoom_changed.emit(self.zoom_factor)
                    event.accept()
                    return
            
            # Pass other key events to the web view
            super().keyPressEvent(event)
        except Exception as e:
            print(f"Error in keyPressEvent: {e}")
            super().keyPressEvent(event)

    def reset_zoom(self):
        """Reset zoom to 100%"""
        try:
            self.zoom_factor = 1.0
            self.setZoomFactor(self.zoom_factor)
            config.set_config_value("zoom_factor", self.zoom_factor)
            self.zoom_changed.emit(self.zoom_factor)
        except Exception as e:
            print(f"Error resetting zoom: {e}")

    def zoom_in(self):
        """Zoom in by one step"""
        try:
            self.zoom_factor = min(self.zoom_factor + 0.1, 5.0)
            self.setZoomFactor(self.zoom_factor)
            config.set_config_value("zoom_factor", self.zoom_factor)
            self.zoom_changed.emit(self.zoom_factor)
        except Exception as e:
            print(f"Error zooming in: {e}")

    def zoom_out(self):
        """Zoom out by one step"""
        try:
            self.zoom_factor = max(self.zoom_factor - 0.1, 0.25)
            self.setZoomFactor(self.zoom_factor)
            config.set_config_value("zoom_factor", self.zoom_factor)  # Fixed: was missing config. prefix
            self.zoom_changed.emit(self.zoom_factor)
        except Exception as e:
            print(f"Error zooming out: {e}")

    def get_zoom_percentage(self):
        """Get current zoom as percentage string"""
        try:
            return f"{int(self.zoom_factor * 100)}%"
        except Exception as e:
            print(f"Error getting zoom percentage: {e}")
            return "100%"