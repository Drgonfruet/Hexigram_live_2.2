# Hexagrams Live 2.2

A comprehensive real-time I Ching hexagram calculator with advanced GUI interface, sound effects, VRChat integration, and multiple time cycle calculations.

## 📁 Repository Structure

### **Root Directory Files**
- **`Hexagrams_Live_2.2.exe`** - Windows executable (34MB) - Ready-to-run program for Windows users
- **`hexagrams_live.zip`** - Complete project archive (7.1MB) - Alternative download with source code
- **`README.md`** - This documentation file

### **Source Code Directory: `Hexagrams_Live_2.2/`**

#### **Core Application Files**
- **`main.py`** - Main application entry point with multi-threaded architecture
- **`constants.py`** - Global configuration, themes, and hexagram definitions
- **`gui_manager.py`** - Complete GUI interface with dark theme and advanced controls
- **`hexagram_calculator.py`** - Core I Ching calculation engine
- **`sound_manager.py`** - Audio system with pygame integration
- **`vrchat_manager.py`** - VRChat OSC communication module

#### **Assets & Resources**
- **`sounds/`** - Audio files for hexagram changes and moving lines
- **`hexagram_images/`** - Visual hexagram GIF images for GUI display
- **`icon.ico`** - Application icon for Windows taskbar

#### **Build Files**
- **`Hexagrams_Live_2.2.spec`** - PyInstaller specification file
- **`build/`** - PyInstaller build artifacts (not included in distribution)

## 🚀 Quick Start

### **For End Users (Windows)**
1. **Download** `Hexagrams_Live_2.2.exe` from the root directory
2. **Double-click** to run - no installation required
3. **Enjoy** real-time hexagram calculations with GUI interface

### **For Developers**
1. **Clone** the repository: `git clone https://github.com/Drgonfruet/Hexigram_live_2.2.git`
2. **Install dependencies**: `pip install pygame python-osc`
3. **Run from source**: `python main.py`

## 🎯 Key Features

### **Real-Time Calculations**
- **6 Time Cycles**: Levels 1-6 with millisecond to day precision
- **Moving Lines**: Dynamic line calculations for each hexagram
- **Zero Date System**: Customizable reference point (default: 2055-07-16)

### **Advanced GUI**
- **Dark Theme**: Modern, professional interface
- **Visual Hexagrams**: GIF images for each of the 64 hexagrams
- **Dual Page System**: Different VRChat message formats
- **Copy to Clipboard**: Easy data sharing functionality

### **Audio System**
- **Individual Controls**: Enable/disable audio for each level (1-6)
- **Moving Line Audio**: Separate controls for line change sounds
- **Pygame Integration**: Reliable audio playback with MP3 support

### **VRChat Integration**
- **OSC Protocol**: Real-time communication with VRChat
- **Dual Message Formats**: Page 1 & Page 2 for different displays
- **Configurable Settings**: IP/Port customization (default: 127.0.0.1:9000)

## 🛠️ Advanced Tools

### **Zero Date Calculator**
- Built-in calculator for determining new reference dates
- 67 years + 104.25 days calculation formula
- Immediate recalculation and display updates

### **Hexagram Checker**
- Historical hexagram lookup for any date/time
- Visual hexagram display with detailed timing
- Moving line calculations with precise timing

### **Sound Management**
- Individual level controls (Levels 1-6)
- Moving line audio controls for each level
- Real-time audio toggles without restart

## 📊 Technical Specifications

### **Performance**
- **Update Frequency**: GUI updates every 0.05 seconds
- **VRChat Messages**: Sent every 2 seconds when enabled
- **Threading**: Separate threads for GUI, VRChat, and main application
- **Memory Usage**: Efficient image caching and sound management

### **Compatibility**
- **Operating Systems**: Windows, macOS, Linux
- **Python Versions**: 3.7, 3.8, 3.9, 3.10, 3.11
- **Dependencies**: Minimal external dependencies for maximum compatibility

## 🔧 Configuration

### **Audio Settings**
- **Level Audio**: Enable/disable sound for hexagram changes at each level
- **Moving Line Audio**: Enable/disable sound for moving line changes
- **Default Settings**: Levels 2-5 enabled by default, Level 1 and 6 disabled

### **VRChat Settings**
- **IP Address**: Default 127.0.0.1 (localhost)
- **Port**: Default 9000
- **Message Format**: Two different page formats for different VRChat displays

### **Display Settings**
- **Theme**: Dark theme by default with professional color scheme
- **Window Size**: Minimum 800x600, default 1280x820
- **Auto-centering**: Window automatically centers on screen

## 📈 Version History

### **Version 2.2 Changes**
- **Complete GUI redesign** with modern dark theme
- **Multi-threaded architecture** for improved performance
- **Advanced audio system** with individual level controls
- **VRChat integration** with dual message formats
- **Zero date calculator** for easy configuration
- **Historical hexagram checker** for date analysis
- **Comprehensive error handling** and stability improvements
- **Professional file organization** and code structure

### **Previous Versions**
- **Version 1.x**: Basic hexagram calculation with simple interface
- **Version 2.0**: Initial advanced features and professional interface

## 🐛 Troubleshooting

### **Common Issues**
1. **Audio not working**: Ensure pygame is installed and audio files are present
2. **VRChat not receiving messages**: Check IP/port settings and VRChat OSC configuration
3. **GUI not displaying**: Ensure tkinter is available in your Python installation
4. **Performance issues**: Close other applications to free up system resources

### **Getting Help**
- Check the console output for error messages
- Verify all required files are present in the correct directories
- Ensure Python dependencies are properly installed
- Test with default settings before making customizations

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Hexagrams Live 2.2** represents a complete evolution of the I Ching hexagram calculator, providing professional-grade tools for real-time hexagram analysis with modern interface design and comprehensive feature set.
