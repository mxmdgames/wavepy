# SurfCast Pro 🌊

A professional desktop surf forecasting application built with Python and PyQt5. Get real-time surf conditions, forecasts, and detailed analysis for surf spots worldwide.

## Features

### 🌍 **Global Surf Spot Database**
- 225+ preloaded surf spots across 45+ countries
- Focus on Costa Rica and Puerto Rico with 25 premium spots
- Worldwide coverage including North/South America, Europe, Africa, Asia, and Oceania
- Remote and specialty big wave spots included

### 📊 **Comprehensive Surf Data**
- **Wave Conditions**: Height, direction, period
- **Swell Analysis**: Primary swell height, direction, period
- **Wind Data**: Speed, direction, wind wave analysis
- **Weather**: Temperature, humidity, precipitation, visibility
- **Tides**: Sunrise/sunset times

### 🎯 **Smart Features**
- **Real-time Search**: Find any surf spot globally with Nominatim integration
- **Favorites System**: Save and quickly access your favorite spots
- **Multiple Forecast Durations**: 3, 5, or 7-day forecasts
- **Visual Direction Indicators**: Arrow-based direction displays
- **Wave Trend Charts**: 24-hour ASCII wave height charts
- **Condition Analysis**: Swell vs wind wave percentages

### 🖥️ **User Interface**
- Modern gradient-based design with surf-inspired colors
- Tabbed interface (Current, Forecast, Details)
- Responsive grid layout for condition widgets
- Scrollable forecast display
- Search results dropdown with autocomplete
- Status bar with real-time updates

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Step 1: Install Python Dependencies
```bash
pip install PyQt5 requests
```

### Step 2: Run the Application
```bash
python surfcast.py
```

## Usage Guide

### 1. **Searching for Surf Spots**
- Type in the search box (minimum 2 characters)
- Results appear in dropdown (debounced for efficiency)
- Click any result to load conditions

### 2. **Viewing Conditions**
- **Current Tab**: Real-time conditions with visual indicators
- **Forecast Tab**: Multi-day forecasts grouped by day
- **Details Tab**: Comprehensive numerical data and analysis

### 3. **Managing Favorites**
- Click "Add to Favorites" to save current location
- Click "⭐ Favorites" button to view/select saved spots
- Favorites persist between sessions

### 4. **Adjusting Forecast Duration**
- Use the dropdown to select 3, 5, or 7-day forecasts
- Automatically refreshes data

## Data Sources

### Open-Meteo Marine API
- Wave height, direction, period
- Swell and wind wave components
- Marine-specific forecasts

### Open-Meteo Weather API
- Temperature, humidity, precipitation
- Wind speed and direction
- Weather codes and visibility

### Nominatim (OpenStreetMap)
- Location search and geocoding
- Global place name resolution

## Technical Details

### Architecture
- **Main Thread**: UI management and user interactions
- **Background Threads**: Data fetching and location searching
- **Caching**: In-memory cache for search results
- **Settings**: Persistent storage for favorites using QSettings

### Key Components
- `DataFetcher`: Fetches marine and weather data in background
- `LocationSearcher`: Handles location search with caching
- `SurfConditionWidget`: Displays surf metrics with styling
- `DirectionWidget`: Shows directional data with arrows
- `SurfCastApp`: Main application class with all UI components

### Styling
- Custom QSS stylesheets for ocean-inspired theme
- Gradient backgrounds and translucent effects
- Consistent color scheme (#00BCD4 blue theme)
- Responsive widget sizing

## Performance Features
- **Debounced Search**: 500ms delay after typing
- **Background Fetching**: Non-blocking data retrieval
- **Memory Caching**: Redundant API calls avoided
- **Error Handling**: Graceful degradation on network issues

## Customization

### Adding More Surf Spots
Edit the `POPULAR_SURF_SPOTS` list to add custom locations:
```python
{"name": "Your Spot", "lat": 12.3456, "lng": -98.7654, "type": "Beach Break", "swell": "SW"}
```

### Modifying Colors
Edit the `setup_styling()` method to change color schemes:
```python
color_scheme = {
    'primary': '#YourColor',
    'secondary': '#YourColor',
    'background': '#YourColor'
}
```

## Troubleshooting

### Common Issues

1. **No Data Loading**
   - Check internet connection
   - Verify API endpoints are accessible
   - Check firewall settings

2. **Search Not Working**
   - Ensure minimum 2 characters entered
   - Check network connectivity to Nominatim
   - Verify user agent compliance

3. **Application Freezes**
   - Ensure background threads are properly managed
   - Check for excessive memory usage
   - Verify Python and PyQt5 versions

### Error Messages
- "Failed to fetch data": API connection issue
- "Search timed out": Network or Nominatim issue
- "Data unavailable": Missing data in API response

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

### Areas for Improvement
- Add map integration
- Include tide data
- Implement alerts/notifications
- Add screenshot/save functionality
- Integrate surf camera feeds

## License

This project is for educational and personal use. Commercial use may require additional licensing for API services.

## Acknowledgments

- Open-Meteo for free weather and marine APIs
- OpenStreetMap for location data
- PyQt5 community for GUI framework
- Surf forecasting community worldwide

## Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Review the code comments
3. Submit a GitHub issue (if applicable)

---

**Happy Surfing!** 🏄‍♂️

*Note: Always check local conditions and surf at your own risk. Forecasts are predictions, not guarantees.*
