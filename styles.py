# styles.py
# Dark Pastel Theme Colors
DARK_PASTEL_BROWN = "#4a3428"     # Dark pastel brown
DARK_PASTEL_GREY = "#3a3a3a"      # Dark pastel grey  
DARK_PASTEL_RED = "#8b4a4a"       # Dark pastel red
LIGHTER_BROWN = "#5c4136"         # Slightly lighter brown
LIGHTER_GREY = "#4a4a4a"          # Slightly lighter grey
LIGHTER_RED = "#a55a5a"           # Slightly lighter red
TEXT_COLOR = "#f5e6c0"            # Light beige text
BORDER_COLOR = "#2a2a2a"          # Dark border

MAIN_STYLESHEET = f"""
QMainWindow {{
    background-color: {DARK_PASTEL_BROWN};
    color: {TEXT_COLOR};
}}

/* Custom title bar styling - dark theme */
QMainWindow::title {{
    background-color: {DARK_PASTEL_BROWN};
    color: {TEXT_COLOR};
}}

QWidget {{
    background-color: {DARK_PASTEL_BROWN};
    color: {TEXT_COLOR};
    font-family: 'RuneScape UF', 'runescape_uf', 'Arial', sans-serif;
    font-size: 12px;
}}

/* Force RuneScape font on all text elements */
QLabel, QPushButton, QCheckBox, QGroupBox, QTabWidget, QTabBar {{
    font-family: 'RuneScape UF', 'runescape_uf', 'Arial', sans-serif;
}}

QTabWidget::tab-bar {{
    font-family: 'RuneScape UF', 'runescape_uf', 'Arial', sans-serif;
}}

QTabBar::tab {{
    font-family: 'RuneScape UF', 'runescape_uf', 'Arial', sans-serif;
    font-weight: bold;
}}

/* Force font on window titles and all text */
* {{
    font-family: 'RuneScape UF', 'runescape_uf', 'Arial', sans-serif;
}}

QSplitter {{
    background-color: {DARK_PASTEL_BROWN};
}}

QSplitter::handle {{
    background-color: {BORDER_COLOR};
    width: 3px;
}}

QSplitter::handle:hover {{
    background-color: {DARK_PASTEL_RED};
}}

/* Tool Panel Styling */
QScrollArea {{
    background-color: {DARK_PASTEL_GREY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 5px;
}}

QScrollArea > QWidget > QWidget {{
    background-color: {DARK_PASTEL_GREY};
}}

/* Tool Buttons */
QPushButton {{
    background-color: {DARK_PASTEL_RED};
    border: 2px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 8px;
    color: {TEXT_COLOR};
    font-weight: bold;
    min-height: 40px;
    text-align: left;
}}

QPushButton:hover {{
    background-color: {LIGHTER_RED};
    border-color: {DARK_PASTEL_RED};
}}

QPushButton:pressed {{
    background-color: {DARK_PASTEL_RED};
    border: 2px inset {BORDER_COLOR};
}}

/* Settings Panel */
QGroupBox {{
    color: {TEXT_COLOR};
    font-weight: bold;
    border: 2px solid {BORDER_COLOR};
    border-radius: 5px;
    margin: 5px 0px;
    padding-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 10px 0 10px;
}}

QCheckBox {{
    color: {TEXT_COLOR};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
}}

QCheckBox::indicator:unchecked {{
    background-color: {DARK_PASTEL_GREY};
    border: 2px solid {BORDER_COLOR};
    border-radius: 3px;
}}

QCheckBox::indicator:checked {{
    background-color: {DARK_PASTEL_RED};
    border: 2px solid {BORDER_COLOR};
    border-radius: 3px;
}}

/* Tool Windows */
QWebEngineView {{
    border: 1px solid {BORDER_COLOR};
}}
"""

def get_icon_path(tool_name):
    """Return the icon path for a tool, with fallback"""
    icon_map = {
        "Clue Coordinates": "📍",
        "Clue Scroll Help": "📜", 
        "World Map": "🗺️",
        "Highscores": "🏆",
        "Market Prices": "💰",
        "Quest Help": "🛡️",  # Changed from sword to shield to avoid duplication
        "Skill Guides": "📚",
        "Forums": "💬",
        "Skills Calculator": "🧮",
        "Bestiary": "🐉"
    }
    return icon_map.get(tool_name, "🔧")