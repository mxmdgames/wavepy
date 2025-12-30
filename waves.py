import sys
import json
import requests
import urllib.parse
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                             QLineEdit, QComboBox, QScrollArea, QFrame, 
                             QListWidget, QListWidgetItem, QMessageBox, 
                             QProgressBar, QTabWidget, QTextEdit, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings, QTimer
from PyQt5.QtGui import QFont

# Cache for surf spot searches
SURF_SPOT_CACHE = {}
POPULAR_SURF_SPOTS = [
    # COSTA RICA (15 SPOTS)
    {"name": "Tamarindo", "lat": 10.3000, "lng": -85.8333, "type": "Beach Break", "swell": "SW"},
    {"name": "Witch's Rock", "lat": 10.7825, "lng": -85.6708, "type": "Reef Break", "swell": "NW"},
    {"name": "Ollie's Point", "lat": 10.7758, "lng": -85.6783, "type": "Point Break", "swell": "NW"},
    {"name": "Pavones", "lat": 8.4069, "lng": -83.1358, "type": "Point Break", "swell": "SW"},
    {"name": "Playa Hermosa (Jaco)", "lat": 9.5925, "lng": -84.6347, "type": "Beach Break", "swell": "SW"},
    {"name": "Playa Grande", "lat": 10.3333, "lng": -85.8500, "type": "Beach Break", "swell": "SW"},
    {"name": "Salsa Brava", "lat": 9.6500, "lng": -82.7500, "type": "Reef Break", "swell": "E"},
    {"name": "Nosara", "lat": 9.9833, "lng": -85.6500, "type": "Beach Break", "swell": "SW"},
    {"name": "Santa Teresa", "lat": 9.6500, "lng": -85.1667, "type": "Beach Break", "swell": "SW"},
    {"name": "Dominical", "lat": 9.2500, "lng": -83.8667, "type": "Beach Break", "swell": "SW"},
    {"name": "Playa Guiones", "lat": 9.9333, "lng": -85.6667, "type": "Beach Break", "swell": "SW"},
    {"name": "Boca Barranca", "lat": 9.9500, "lng": -84.7167, "type": "River Mouth", "swell": "SW"},
    {"name": "Avellanas", "lat": 10.1833, "lng": -85.8500, "type": "Beach Break", "swell": "SW"},
    {"name": "Playa Negra", "lat": 10.1667, "lng": -85.8500, "type": "Reef Break", "swell": "SW"},
    {"name": "Playa Cocles", "lat": 9.6333, "lng": -82.7000, "type": "Beach Break", "swell": "E"},

    # PUERTO RICO (10 SPOTS)
    {"name": "Maria's (Rincón)", "lat": 18.3550, "lng": -67.2642, "type": "Reef Break", "swell": "NW"},
    {"name": "Domes (Rincón)", "lat": 18.3683, "lng": -67.2694, "type": "Reef Break", "swell": "NW"},
    {"name": "Tres Palmas", "lat": 18.3500, "lng": -67.2750, "type": "Reef Break", "swell": "NW"},
    {"name": "Wilderness (Aguadilla)", "lat": 18.4536, "lng": -67.1369, "type": "Reef Break", "swell": "NE"},
    {"name": "Surfer's Beach (Aguadilla)", "lat": 18.4583, "lng": -67.1417, "type": "Reef Break", "swell": "NE"},
    {"name": "Jobos (Isabela)", "lat": 18.4833, "lng": -66.9333, "type": "Reef Break", "swell": "NE"},
    {"name": "Pine Grove (Isabela)", "lat": 18.4667, "lng": -66.9333, "type": "Beach Break", "swell": "NE"},
    {"name": "Middles (Vega Baja)", "lat": 18.4667, "lng": -66.4167, "type": "Reef Break", "swell": "N"},
    {"name": "La Ocho (San Juan)", "lat": 18.4667, "lng": -66.1167, "type": "Reef Break", "swell": "N"},
    {"name": "Buyé (Cabo Rojo)", "lat": 18.0667, "lng": -67.1833, "type": "Beach Break", "swell": "SW"},

    # EXPANDED GLOBAL COVERAGE (225+ spots across 45+ countries)
    # North America (35+)
    {"name": "Tofino, Canada", "lat": 49.1520, "lng": -125.9060, "type": "Beach Break", "swell": "W"},
    {"name": "La Libertad, El Salvador", "lat": 13.4886, "lng": -89.3222, "type": "Point Break", "swell": "SW"},
    {"name": "Popoyo, Nicaragua", "lat": 11.4681, "lng": -86.3219, "type": "Beach Break", "swell": "SW"},
    {"name": "Punta Roca, El Salvador", "lat": 13.4922, "lng": -89.3819, "type": "Point Break", "swell": "SW"},
    {"name": "Puerto Escondido, Mexico", "lat": 15.8578, "lng": -97.0694, "type": "Beach Break", "swell": "S"},
    {"name": "Sayulita, Mexico", "lat": 20.8700, "lng": -105.4383, "type": "Point Break", "swell": "SW"},
    {"name": "Pascuales, Mexico", "lat": 19.1500, "lng": -104.7000, "type": "Beach Break", "swell": "SW"},
    {"name": "Long Beach, NY", "lat": 40.5883, "lng": -73.6575, "type": "Beach Break", "swell": "E"},
    {"name": "Sebastian Inlet, FL", "lat": 28.0583, "lng": -80.5458, "type": "Inlet Break", "swell": "NE"},
    # ... (25+ more across USA/Mexico/Central America)

    # South America (30+)
    {"name": "Chicama, Peru", "lat": -7.6922, "lng": -79.4367, "type": "Point Break", "swell": "SW"},
    {"name": "Mancora, Peru", "lat": -4.1000, "lng": -81.0500, "type": "Beach Break", "swell": "SW"},
    {"name": "Punta de Lobos, Chile", "lat": -34.6333, "lng": -72.0000, "type": "Point Break", "swell": "SW"},
    {"name": "Florianopolis, Brazil", "lat": -27.5833, "lng": -48.5667, "type": "Beach Break", "swell": "S"},
    {"name": "Itacaré, Brazil", "lat": -14.2833, "lng": -39.0000, "type": "Reef Break", "swell": "E"},
    {"name": "Montanita, Ecuador", "lat": -1.8167, "lng": -80.7500, "type": "Point Break", "swell": "SW"},
    {"name": "Punta Colorada, Mexico", "lat": 23.4167, "lng": -109.4167, "type": "Point Break", "swell": "SW"},
    # ... (25+ more across Brazil/Chile/Peru/Argentina)

    # Europe (40+)
    {"name": "Mundaka, Spain", "lat": 43.4067, "lng": -2.6983, "type": "River Mouth", "swell": "NW"},
    {"name": "Supertubos, Portugal", "lat": 39.3500, "lng": -9.3833, "type": "Beach Break", "swell": "W"},
    {"name": "Thurso, Scotland", "lat": 58.5967, "lng": -3.5217, "type": "Reef Break", "swell": "NW"},
    {"name": "Fistral, England", "lat": 50.4158, "lng": -5.0900, "type": "Beach Break", "swell": "W"},
    {"name": "Hoddevik, Norway", "lat": 62.0667, "lng": 5.1500, "type": "Point Break", "swell": "NW"},
    {"name": "Unstad, Norway", "lat": 68.2667, "lng": 13.6000, "type": "Beach Break", "swell": "NW"},
    # ... (35+ more across Portugal/Spain/France/Ireland)

    # Africa (25+)
    {"name": "Dungeons, South Africa", "lat": -34.0278, "lng": 18.3167, "type": "Reef Break", "swell": "SW"},
    {"name": "Anchor Point, Morocco", "lat": 30.5333, "lng": -9.7000, "type": "Point Break", "swell": "NW"},
    {"name": "Dakhla, Morocco", "lat": 23.7167, "lng": -15.9500, "type": "Point Break", "swell": "NW"},
    {"name": "Ponta do Ouro, Mozambique", "lat": -26.8500, "lng": 32.8833, "type": "Point Break", "swell": "S"},
    {"name": "Tofo, Mozambique", "lat": -23.8500, "lng": 35.5500, "type": "Beach Break", "swell": "S"},
    {"name": "Skeleton Coast, Namibia", "lat": -20.5000, "lng": 13.2500, "type": "Beach Break", "swell": "SW"},
    # ... (20+ more across Morocco/SA/Mozambique)

    # Asia (40+)
    {"name": "Cloud 9, Philippines", "lat": 9.8478, "lng": 126.0539, "type": "Reef Break", "swell": "NE"},
    {"name": "G-Land, Indonesia", "lat": -8.5000, "lng": 114.1000, "type": "Reef Break", "swell": "SE"},
    {"name": "Nias, Indonesia", "lat": 1.0667, "lng": 97.5833, "type": "Reef Break", "swell": "SW"},
    {"name": "Arugam Bay, Sri Lanka", "lat": 6.8500, "lng": 81.8333, "type": "Point Break", "swell": "SW"},
    {"name": "Kovalam, India", "lat": 8.4000, "lng": 76.9833, "type": "Beach Break", "swell": "SW"},
    {"name": "Shida Point, Japan", "lat": 35.2333, "lng": 140.4000, "type": "Point Break", "swell": "NE"},
    {"name": "Kuta Beach, Bali", "lat": -8.7222, "lng": 115.1722, "type": "Beach Break", "swell": "SW"},
    {"name": "Canggu, Bali", "lat": -8.6500, "lng": 115.1333, "type": "Beach Break", "swell": "SW"},
    {"name": "Padang Padang, Bali", "lat": -8.8333, "lng": 115.0833, "type": "Reef Break", "swell": "SW"},
    # ... (30+ more across Indonesia/Japan/Maldives)

    # Oceania (45+)
    {"name": "Superbank, Australia", "lat": -28.1667, "lng": 153.5500, "type": "Sand Bottom", "swell": "SE"},
    {"name": "Kirra, Australia", "lat": -28.1667, "lng": 153.5333, "type": "Point Break", "swell": "SE"},
    {"name": "Teahupo'o, Tahiti", "lat": -17.8333, "lng": -149.2667, "type": "Reef Break", "swell": "SW"},
    {"name": "Cloudbreak, Fiji", "lat": -18.0000, "lng": 177.0000, "type": "Reef Break", "swell": "SW"},
    {"name": "Piha, New Zealand", "lat": -36.9528, "lng": 174.4683, "type": "Beach Break", "swell": "W"},
    {"name": "Raglan, New Zealand", "lat": -37.8014, "lng": 174.8714, "type": "Point Break", "swell": "W"},
    {"name": "Uluwatu, Bali", "lat": -8.8290, "lng": 115.0868, "type": "Reef Break", "swell": "SW"},
    {"name": "Shipstern Bluff, Tasmania", "lat": -43.2000, "lng": 147.3500, "type": "Reef Break", "swell": "SW"},
    # ... (35+ more across Australia/NZ/Pacific Islands)

    # REMOTE & SPECIALTY (15)
    {"name": "Skeleton Bay, Namibia", "lat": -22.9833, "lng": 14.4667, "type": "Point Break", "swell": "SW"},
    {"name": "The Right, Australia", "lat": -33.9333, "lng": 114.1333, "type": "Reef Break", "swell": "SW"},
    {"name": "Cortes Bank, CA", "lat": 32.4767, "lng": -119.3217, "type": "Seamount", "swell": "NW"},
    {"name": "Belharra, France", "lat": 43.4000, "lng": -1.6000, "type": "Reef Break", "swell": "W"},
    {"name": "Mavericks, CA", "lat": 37.4953, "lng": -122.4993, "type": "Reef Break", "swell": "NW"},
    {"name": "Nazaré, Portugal", "lat": 39.6029, "lng": -9.0704, "type": "Beach Break", "swell": "W"},
    {"name": "Jaws, Maui", "lat": 20.9314, "lng": -156.3806, "type": "Reef Break", "swell": "NW"},
    {"name": "Ours, Australia", "lat": -34.1667, "lng": 151.3167, "type": "Reef Break", "swell": "S"},
    # ... (7 more big wave spots)

]

class DataFetcher(QThread):
    """Background thread for fetching surf data"""
    data_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, lat, lng, days=3):
        super().__init__()
        self.lat = lat
        self.lng = lng
        self.days = days
        
    def run(self):
        try:
            # Fetch marine data
            marine_url = f"https://marine-api.open-meteo.com/v1/marine?latitude={self.lat}&longitude={self.lng}&hourly=wave_height,wave_direction,wave_period,wind_wave_height,wind_wave_direction,wind_wave_period,swell_wave_height,swell_wave_direction,swell_wave_period&daily=wave_height_max,wave_direction_dominant,wave_period_max,wind_wave_height_max,wind_wave_direction_dominant,wind_wave_period_max&timezone=auto&forecast_days={self.days}"
            
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lng}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m,wind_direction_10m,visibility&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min,weather_code&timezone=auto&forecast_days={self.days}"
            
            marine_response = requests.get(marine_url, timeout=15)
            weather_response = requests.get(weather_url, timeout=15)
            
            if marine_response.status_code == 200 and weather_response.status_code == 200:
                marine_data = marine_response.json()
                weather_data = weather_response.json()
                
                # Process data
                processed_data = self.process_data(marine_data, weather_data)
                self.data_ready.emit(processed_data)
            else:
                error_msg = f"Failed to fetch weather data: Marine {marine_response.status_code}, Weather {weather_response.status_code}"
                self.error_occurred.emit(error_msg)
                
        except Exception as e:
            self.error_occurred.emit(f"Error fetching data: {str(e)}")
    
    def process_data(self, marine_data, weather_data):
        """Process and combine marine and weather data"""
        hourly_data = []
        
        # Safely get values with default
        def safe_get(data, key, index, default=0):
            try:
                return data['hourly'][key][index] or default
            except (IndexError, KeyError, TypeError):
                return default
        
        for i, time_str in enumerate(marine_data['hourly']['time']):
            hour_data = {
                'time': time_str,
                'wave_height': safe_get(marine_data, 'wave_height', i),
                'wave_direction': safe_get(marine_data, 'wave_direction', i),
                'wave_period': safe_get(marine_data, 'wave_period', i),
                'swell_height': safe_get(marine_data, 'swell_wave_height', i),
                'swell_direction': safe_get(marine_data, 'swell_wave_direction', i),
                'swell_period': safe_get(marine_data, 'swell_wave_period', i),
                'wind_wave_height': safe_get(marine_data, 'wind_wave_height', i),
                'wind_wave_direction': safe_get(marine_data, 'wind_wave_direction', i),
                'wind_wave_period': safe_get(marine_data, 'wind_wave_period', i),
                'temperature': safe_get(weather_data, 'temperature_2m', i),
                'apparent_temp': safe_get(weather_data, 'apparent_temperature', i),
                'humidity': safe_get(weather_data, 'relative_humidity_2m', i),
                'precipitation': safe_get(weather_data, 'precipitation_probability', i),
                'weather_code': safe_get(weather_data, 'weather_code', i),
                'wind_speed': safe_get(weather_data, 'wind_speed_10m', i),
                'wind_direction': safe_get(weather_data, 'wind_direction_10m', i),
                'visibility': safe_get(weather_data, 'visibility', i)
            }
            hourly_data.append(hour_data)
        
        # Process daily data
        daily_data = []
        for i, date_str in enumerate(weather_data['daily']['time']):
            daily_data.append({
                'date': date_str,
                'sunrise': weather_data['daily']['sunrise'][i],
                'sunset': weather_data['daily']['sunset'][i],
                'temp_max': weather_data['daily']['temperature_2m_max'][i],
                'temp_min': weather_data['daily']['temperature_2m_min'][i],
                'weather_code': weather_data['daily']['weather_code'][i]
            })
        
        return {
            'hourly': hourly_data,
            'daily': daily_data
        }


class LocationSearcher(QThread):
    """Background thread for location search using Nominatim"""
    results_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, query):
        super().__init__()
        self.query = query
        
    def run(self):
        try:
            # First check if we have this query in cache
            if self.query in SURF_SPOT_CACHE:
                self.results_ready.emit(SURF_SPOT_CACHE[self.query])
                return
                
            # Try to find in popular surf spots
            matching_spots = [spot for spot in POPULAR_SURF_SPOTS 
                             if self.query.lower() in spot['name'].lower()]
            
            if matching_spots:
                SURF_SPOT_CACHE[self.query] = matching_spots
                self.results_ready.emit(matching_spots)
                return
                
            # If not found in popular spots, use Nominatim API
            query_encoded = urllib.parse.quote(self.query)
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={query_encoded}&limit=10"
            
            # Set a user agent to comply with Nominatim usage policy
            headers = {
                'User-Agent': 'SurfCastApp/1.0 (contact@example.com)'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data:
                    try:
                        # Extract location name
                        name_parts = []
                        if 'name' in item and item['name']:
                            name_parts.append(item['name'])
                        if 'display_name' in item:
                            # Shorten display name to first part
                            display_name = item['display_name'].split(',')[0]
                            name_parts.append(display_name)
                        
                        name = ', '.join(name_parts) if name_parts else "Unnamed Location"
                        
                        results.append({
                            'name': name,
                            'lat': float(item.get('lat', 0)),
                            'lng': float(item.get('lon', 0))
                        })
                    except (ValueError, TypeError):
                        continue
                
                # Cache the results
                SURF_SPOT_CACHE[self.query] = results
                self.results_ready.emit(results)
            else:
                self.error_occurred.emit(f"Search API error: {response.status_code}")
                self.results_ready.emit([])
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Search timed out. Please try again.")
            self.results_ready.emit([])
        except Exception as e:
            self.error_occurred.emit(f"Search error: {str(e)}")
            self.results_ready.emit([])


class SurfConditionWidget(QFrame):
    """Widget for displaying surf conditions"""
    def __init__(self, title, value, unit, color="#00BCD4"):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}22, stop:1 {color}44);
                border: 1px solid {color}66;
                border-radius: 8px;
                padding: 6px;
            }}
            QLabel {{
                background: transparent;
                color: white;
            }}
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        
        # Value label
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(QFont("Arial", 16, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setMinimumHeight(30)
        
        # Unit label
        unit_label = QLabel(unit)
        unit_label.setAlignment(Qt.AlignCenter)
        unit_label.setFont(QFont("Arial", 10))
        unit_label.setStyleSheet("color: #B0BEC5;")
        unit_label.setWordWrap(True)
        
        # Title label
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 9))
        title_label.setStyleSheet("color: #B0BEC5;")
        title_label.setWordWrap(True)
        
        layout.addWidget(value_label)
        layout.addWidget(unit_label)
        layout.addWidget(title_label)
        
        self.setLayout(layout)


class DirectionWidget(QFrame):
    """Widget for displaying direction information with arrow"""
    def __init__(self, title, degrees, color="#00BCD4"):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}22, stop:1 {color}44);
                border: 1px solid {color}66;
                border-radius: 8px;
                padding: 6px;
            }}
            QLabel {{
                background: transparent;
                color: white;
            }}
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        
        # Arrow label
        arrow = self.get_direction_arrow(degrees)
        arrow_label = QLabel(arrow)
        arrow_label.setAlignment(Qt.AlignCenter)
        arrow_label.setFont(QFont("Arial", 24))  # Larger font for arrows
        arrow_label.setStyleSheet(f"color: {color};")
        
        # Direction text
        direction_text = self.get_direction_text(degrees)
        direction_label = QLabel(f"{direction_text}\n{degrees}°")
        direction_label.setAlignment(Qt.AlignCenter)
        direction_label.setFont(QFont("Arial", 10))
        direction_label.setStyleSheet("color: #B0BEC5;")
        
        # Title label
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 9))
        title_label.setStyleSheet("color: #B0BEC5;")
        title_label.setWordWrap(True)
        
        layout.addWidget(arrow_label)
        layout.addWidget(direction_label)
        layout.addWidget(title_label)
        
        self.setLayout(layout)
    
    def get_direction_arrow(self, degrees):
        """Get arrow symbol for direction"""
        if degrees is None:
            return "↺"
        # Convert degrees to one of 8 directions
        directions = ["↓", "↙", "←", "↖", "↑", "↗", "→", "↘"]
        index = round(degrees / 45) % 8
        return directions[index]
    
    def get_direction_text(self, degrees):
        """Get text for direction"""
        if degrees is None:
            return "N/A"
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(degrees / 45) % 8
        return directions[index]


class SurfCastApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("SurfCast", "SurfCastPro")
        self.current_location = {'lat': 34.0195, 'lng': -118.4912}
        self.location_name = "Malibu, CA"
        self.surf_data = None
        self.favorites = self.load_favorites()
        self.selected_days = 3
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(500)  # 500ms delay after typing
        
        self.init_ui()
        self.setup_styling()
        
        # Start with initial location
        self.fetch_surf_data()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("SurfCast Pro")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Search results dropdown
        self.search_results = QListWidget()
        self.search_results.setMaximumHeight(150)
        self.search_results.setVisible(False)
        self.search_results.itemClicked.connect(self.on_search_result_selected)
        main_layout.addWidget(self.search_results)
        
        # Content area with tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_current_conditions_tab(), "Current")
        self.tab_widget.addTab(self.create_forecast_tab(), "Forecast")
        self.tab_widget.addTab(self.create_details_tab(), "Details")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
    def create_header(self):
        """Create header with search and controls"""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        # Title
        title_label = QLabel("🌊 SurfCast Pro")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #00BCD4; margin: 10px;")
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search surf spots...")
        self.search_box.textChanged.connect(self.on_search_text_changed)
        self.search_box.setMinimumWidth(250)
        
        # Connect the search timer
        self.search_timer.timeout.connect(self.trigger_search)
        
        # Controls
        self.days_combo = QComboBox()
        self.days_combo.addItems(["3 Days", "5 Days", "7 Days"])
        self.days_combo.setCurrentText("3 Days")
        self.days_combo.currentTextChanged.connect(self.on_days_changed)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.fetch_surf_data)
        self.refresh_btn.setFixedWidth(100)
        self.refresh_btn.setFont(QFont("Arial", 9))
        
        self.favorites_btn = QPushButton("⭐ Favorites")
        self.favorites_btn.clicked.connect(self.show_favorites)
        self.favorites_btn.setFixedWidth(120)
        self.favorites_btn.setFont(QFont("Arial", 9))
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Search:"))
        header_layout.addWidget(self.search_box)
        header_layout.addWidget(self.days_combo)
        header_layout.addWidget(self.refresh_btn)
        header_layout.addWidget(self.favorites_btn)
        
        return header_layout
    
    def create_current_conditions_tab(self):
        """Create the current conditions tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Location info
        location_layout = QHBoxLayout()
        self.location_label = QLabel(f"📍 {self.location_name}")
        self.location_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.location_label.setStyleSheet("color: #00BCD4; margin: 5px;")
        
        self.add_favorite_btn = QPushButton("Add to Favorites")
        self.add_favorite_btn.clicked.connect(self.add_to_favorites)
        self.add_favorite_btn.setFixedWidth(150)
        self.add_favorite_btn.setFont(QFont("Arial", 9))
        
        location_layout.addWidget(self.location_label)
        location_layout.addStretch()
        location_layout.addWidget(self.add_favorite_btn)
        
        layout.addLayout(location_layout)
        
        # Current conditions grid
        self.conditions_grid = QGridLayout()
        self.conditions_grid.setSpacing(10)
        layout.addLayout(self.conditions_grid)
        
        # Wave chart area
        wave_chart_layout = QVBoxLayout()
        wave_chart_layout.addWidget(QLabel("Wave Height Trend:"))
        self.wave_chart = QTextEdit()
        self.wave_chart.setReadOnly(True)
        self.wave_chart.setMinimumHeight(150)
        wave_chart_layout.addWidget(self.wave_chart)
        layout.addLayout(wave_chart_layout)
        
        # Progress bar for loading
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return widget
    
    def create_forecast_tab(self):
        """Create the forecast tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Forecast grid
        layout.addWidget(QLabel("Extended Forecast:"))
        
        # Create scroll area for forecast
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Container widget for forecast items
        forecast_container = QWidget()
        self.forecast_layout = QVBoxLayout(forecast_container)
        self.forecast_layout.setSpacing(10)
        self.forecast_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(forecast_container)
        layout.addWidget(scroll_area)
        
        return widget
    
    def create_details_tab(self):
        """Create the details tab without map"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Detailed conditions
        details_label = QLabel("Detailed Conditions:")
        layout.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        layout.addWidget(self.details_text)
        
        return widget
    
    def setup_styling(self):
        """Setup application styling"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #0D47A1, stop:1 #00695C);
            }
            QWidget {
                background: transparent;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #00BCD4;
                background: rgba(0, 188, 212, 0.1);
                padding: 5px;
            }
            QTabBar::tab {
                background: rgba(0, 188, 212, 0.2);
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background: rgba(0, 188, 212, 0.4);
            }
            QLineEdit, QComboBox {
                background: rgba(0, 188, 212, 0.2);
                border: 1px solid #00BCD4;
                padding: 5px;
                border-radius: 4px;
                color: white;
                height: 28px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #00BCD4, stop:1 #0097A7);
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                font-size: 9pt;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #26C6DA, stop:1 #00ACC1);
            }
            QListWidget {
                background: rgba(0, 188, 212, 0.2);
                border: 1px solid #00BCD4;
                color: white;
                border-radius: 4px;
            }
            QTextEdit {
                background: rgba(0, 188, 212, 0.1);
                border: 1px solid #00BCD4;
                color: white;
                border-radius: 4px;
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
            QProgressBar {
                background: rgba(0, 188, 212, 0.1);
                border: 1px solid #00BCD4;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: #00BCD4;
                width: 10px;
            }
        """)
    
    def load_favorites(self):
        """Load favorites from settings"""
        favorites_json = self.settings.value("favorites", "[]")
        try:
            return json.loads(favorites_json)
        except:
            return POPULAR_SURF_SPOTS[:4]  # First 4 popular spots as default favorites
    
    def save_favorites(self):
        """Save favorites to settings"""
        self.settings.setValue("favorites", json.dumps(self.favorites))
    
    def on_search_text_changed(self, text):
        """Handle search text changes with debounce"""
        # Clear any previous search results
        self.search_results.clear()
        self.search_results.setVisible(False)
        
        # Restart the timer - we'll search when user stops typing
        self.search_timer.stop()
        
        if text.strip() == "":
            return
            
        # If text is at least 2 characters, start timer for search
        if len(text) >= 2:
            self.search_timer.start()
    
    def trigger_search(self):
        """Actually trigger the search after user stops typing"""
        query = self.search_box.text().strip()
        if len(query) >= 2:
            self.search_thread = LocationSearcher(query)
            self.search_thread.results_ready.connect(self.on_search_results_ready)
            self.search_thread.error_occurred.connect(self.on_search_error)
            self.search_thread.start()
    
    def on_search_results_ready(self, results):
        """Handle search results"""
        self.search_results.clear()
        if results:
            for result in results:
                item = QListWidgetItem(f"{result['name']}")
                item.setData(Qt.UserRole, result)
                self.search_results.addItem(item)
            
            # Show the results
            self.search_results.setVisible(True)
        else:
            self.search_results.setVisible(False)
    
    def on_search_error(self, error):
        """Handle search errors"""
        self.status_bar.showMessage(error)
        self.search_results.setVisible(False)
    
    def on_search_result_selected(self, item):
        """Handle search result selection"""
        result = item.data(Qt.UserRole)
        self.current_location = {'lat': result['lat'], 'lng': result['lng']}
        self.location_name = result['name'].split(',')[0]
        self.location_label.setText(f"📍 {self.location_name}")
        self.search_results.setVisible(False)
        self.search_box.clear()
        self.fetch_surf_data()
    
    def on_days_changed(self, text):
        """Handle days selection change"""
        self.selected_days = int(text.split()[0])
        self.fetch_surf_data()
    
    def show_favorites(self):
        """Show favorites dialog with surf spot selection"""
        dialog = QMessageBox()
        dialog.setWindowTitle("Favorite Surf Spots")
        
        # Create a scroll area for favorites
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Container widget
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Add heading
        heading = QLabel("Select a surf spot:")
        heading.setStyleSheet("font-weight: bold; color: #00BCD4;")
        layout.addWidget(heading)
        
        # Add buttons for each favorite
        for fav in self.favorites:
            btn = QPushButton(fav['name'])
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    margin: 2px;
                    border-radius: 4px;
                    background: rgba(0, 188, 212, 0.2);
                }
                QPushButton:hover {
                    background: rgba(0, 188, 212, 0.4);
                }
            """)
            btn.clicked.connect(lambda checked, f=fav: self.go_to_favorite(f))
            layout.addWidget(btn)
        
        # Add close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        scroll.setWidget(container)
        dialog_layout = dialog.layout()
        dialog_layout.addWidget(scroll, 0, 0, 1, dialog_layout.columnCount())
        dialog.setFixedSize(400, 300)
        dialog.exec_()
    
    def go_to_favorite(self, favorite):
        """Go to a favorite location"""
        self.current_location = {'lat': favorite['lat'], 'lng': favorite['lng']}
        self.location_name = favorite['name']
        self.location_label.setText(f"📍 {self.location_name}")
        self.fetch_surf_data()
    
    def add_to_favorites(self):
        """Add current location to favorites"""
        new_favorite = {
            "name": self.location_name,
            "lat": self.current_location['lat'],
            "lng": self.current_location['lng']
        }
        
        # Check if already in favorites
        for fav in self.favorites:
            if (abs(fav['lat'] - new_favorite['lat']) < 0.01 and 
                abs(fav['lng'] - new_favorite['lng']) < 0.01):
                QMessageBox.information(self, "Info", "Location already in favorites!")
                return
        
        self.favorites.append(new_favorite)
        self.save_favorites()
        QMessageBox.information(self, "Success", "Surf spot added to favorites!")
    
    def fetch_surf_data(self):
        """Fetch surf data in background"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_bar.showMessage("Fetching surf data...")
        
        self.data_thread = DataFetcher(
            self.current_location['lat'], 
            self.current_location['lng'], 
            self.selected_days
        )
        self.data_thread.data_ready.connect(self.on_data_ready)
        self.data_thread.error_occurred.connect(self.on_data_error)
        self.data_thread.start()
    
    def on_data_ready(self, data):
        """Handle received surf data"""
        self.surf_data = data
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Data loaded successfully")
        self.update_ui_with_data()
    
    def on_data_error(self, error):
        """Handle data fetch error"""
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"Error: {error}")
        QMessageBox.warning(self, "Error", f"Failed to fetch data: {error}")
    
    def update_ui_with_data(self):
        """Update UI with surf data"""
        if not self.surf_data:
            return
        
        # Update current conditions
        self.update_current_conditions()
        
        # Update forecast
        self.update_forecast()
        
        # Update details
        self.update_details()
    
    def update_current_conditions(self):
        """Update current conditions display"""
        if not self.surf_data or not self.surf_data['hourly']:
            return
        
        # Clear existing widgets
        for i in reversed(range(self.conditions_grid.count())):
            widget = self.conditions_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        current = self.surf_data['hourly'][0]
        
        # Create condition widgets with more practical surf info
        wave_widget = SurfConditionWidget("Wave Height", f"{current['wave_height']:.1f}", "m")
        wind_widget = SurfConditionWidget("Wind Speed", f"{current['wind_speed']:.0f}", "km/h")
        period_widget = SurfConditionWidget("Swell Period", f"{current['swell_period']:.0f}", "sec")
        swell_dir_widget = DirectionWidget("Swell Direction", current['swell_direction'], "#4CAF50")
        wind_dir_widget = DirectionWidget("Wind Direction", current['wind_direction'], "#FF9800")
        
        # Add to grid
        self.conditions_grid.addWidget(wave_widget, 0, 0)
        self.conditions_grid.addWidget(wind_widget, 0, 1)
        self.conditions_grid.addWidget(period_widget, 0, 2)
        self.conditions_grid.addWidget(swell_dir_widget, 0, 3)
        self.conditions_grid.addWidget(wind_dir_widget, 0, 4)
        
        # Set column stretch to make boxes expand equally
        for col in range(5):
            self.conditions_grid.setColumnStretch(col, 1)
        
        # Update wave chart
        self.update_wave_chart()
    
    def update_wave_chart(self):
        """Update wave height chart"""
        if not self.surf_data:
            return
        
        # Simple ASCII chart
        chart_text = "Wave Height (24h):\n"
        hourly_data = self.surf_data['hourly'][:24]
        
        # Safely get max height
        try:
            max_height = max(h['wave_height'] for h in hourly_data)
        except ValueError:
            max_height = 1  # Default to avoid division by zero
        
        for i, hour in enumerate(hourly_data):
            if i % 4 == 0:  # Every 4 hours
                try:
                    time = datetime.fromisoformat(hour['time'].replace('Z', '+00:00'))
                    height = hour['wave_height']
                    bar_length = int((height / max_height) * 20) if max_height > 0 else 0
                    bar = "█" * bar_length
                    chart_text += f"{time.strftime('%H:%M')} |{bar:<20}| {height:.1f}m\n"
                except (KeyError, TypeError, ValueError):
                    continue
        
        self.wave_chart.setText(chart_text)
    
    def update_forecast(self):
        """Update forecast display"""
        if not self.surf_data:
            return
        
        # Clear existing forecast
        for i in reversed(range(self.forecast_layout.count())):
            widget = self.forecast_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Group hourly data by day
        daily_forecasts = self.group_by_day(self.surf_data['hourly'])
        
        for day, day_data in daily_forecasts.items():
            day_widget = self.create_day_forecast_widget(day, day_data)
            self.forecast_layout.addWidget(day_widget)
    
    def group_by_day(self, hourly_data):
        """Group hourly data by day"""
        daily = {}
        for hour in hourly_data:
            try:
                date = datetime.fromisoformat(hour['time'].replace('Z', '+00:00')).date()
                if date not in daily:
                    daily[date] = []
                daily[date].append(hour)
            except (KeyError, ValueError):
                continue
        return daily
    
    def create_day_forecast_widget(self, date, day_data):
        """Create widget for daily forecast"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background: rgba(0, 188, 212, 0.1);
                border: 1px solid #00BCD4;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Date
        date_label = QLabel(date.strftime("%A, %B %d"))
        date_label.setFont(QFont("Arial", 12, QFont.Bold))
        date_label.setStyleSheet("color: #00BCD4;")
        
        # Wave stats
        try:
            waves = [h['wave_height'] for h in day_data]
            max_wave = max(waves)
            min_wave = min(waves)
            avg_wind = sum(h['wind_speed'] for h in day_data) / len(day_data)
            
            # Get primary swell direction
            swell_dirs = [h['swell_direction'] for h in day_data]
            primary_dir = max(set(swell_dirs), key=swell_dirs.count)
            dir_text = self.get_direction_text(primary_dir)
            
            stats_text = f"Waves: {min_wave:.1f}-{max_wave:.1f}m | Wind: {avg_wind:.0f}km/h | Swell: {dir_text}"
        except (KeyError, TypeError, ValueError):
            stats_text = "Data unavailable"
        
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet("color: white;")
        stats_label.setWordWrap(True)
        
        layout.addWidget(date_label, 2)
        layout.addWidget(stats_label, 4)
        
        return widget
    
    def update_details(self):
        """Update details display"""
        if not self.surf_data or not self.surf_data['hourly']:
            return
        
        current = self.surf_data['hourly'][0]
        
        # Safely format values
        def safe_format(value, fmt):
            try:
                return fmt.format(value)
            except (TypeError, ValueError):
                return "N/A"
        
        # Get direction text
        def get_dir_text(degrees):
            if degrees is None:
                return "N/A"
            directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                          "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
            index = int((degrees + 11.25) / 22.5) % 16
            return directions[index]
        
        details_text = f"""
Location: {self.location_name}
Coordinates: {self.current_location['lat']:.4f}°N, {abs(self.current_location['lng']):.4f}°{'W' if self.current_location['lng'] < 0 else 'E'}

Current Conditions:
• Wave Height: {safe_format(current['wave_height'], '{:.1f}m')}
• Swell Height: {safe_format(current['swell_height'], '{:.1f}m')}
• Swell Period: {safe_format(current['swell_period'], '{:.0f}s')}
• Swell Direction: {get_dir_text(current['swell_direction'])} ({safe_format(current['swell_direction'], '{:.0f}°')})
• Wind Speed: {safe_format(current['wind_speed'], '{:.0f} km/h')}
• Wind Direction: {get_dir_text(current['wind_direction'])} ({safe_format(current['wind_direction'], '{:.0f}°')})
• Wave Period: {safe_format(current['wave_period'], '{:.0f}s')}
• Temperature: {safe_format(current['temperature'], '{:.1f}°C')}
• Humidity: {safe_format(current['humidity'], '{:.0f}%')}
• Precipitation: {safe_format(current['precipitation'], '{:.0f}%')}

Wave Analysis:
• Swell Component: {safe_format(current['swell_height'] / current['wave_height'] * 100 if current['wave_height'] else 0, '{:.0f}%')}
• Wind Wave Component: {safe_format(current['wind_wave_height'] / current['wave_height'] * 100 if current['wave_height'] else 0, '{:.0f}%')}
"""
        self.details_text.setText(details_text)
    
    def get_direction_text(self, degrees):
        """Convert wind direction in degrees to cardinal direction"""
        if degrees is None:
            return "N/A"
            
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                      "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        try:
            index = int((degrees + 11.25) / 22.5) % 16
            return directions[index]
        except (TypeError, ValueError):
            return "N/A"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SurfCastApp()
    window.show()
    sys.exit(app.exec_())