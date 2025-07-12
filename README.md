
#### **Bug Fixes & Stability**
- **Fixed audio timing issues**: Resolved problems with audio playback during zero date changes
- **Improved error recovery**: Better handling of missing audio files and network connection issues
- **Enhanced GUI responsiveness**: Eliminated freezing issues during heavy calculations
- **Memory leak prevention**: Proper cleanup of resources and thread management

#### **Configuration Changes**
- **New audio flags**: Added PLAY_AUDIO_LEVEL_6_ENABLED and PLAY_AUDIO_LEVEL_6_LINE_ENABLED
- **Updated constants**: Enhanced previous_hexagrams tracking for all levels
- **Window management**: Improved window positioning and sizing logic

### **Backward Compatibility**
- **Maintained core functionality**: All existing features from 2.0 remain functional
- **Preserved file structure**: Existing audio and image files continue to work
- **Configuration compatibility**: Old settings are automatically migrated where possible

### **Installation Notes**
- **Dependencies**: No new dependencies required beyond 2.0 requirements
- **File updates**: Existing installations can be updated by replacing core Python files
- **Configuration**: New audio settings default to Level 6 disabled for compatibility

### **Key Improvements**

1. **Level 6 Integration**: Added support for Level 6 moving line days and moving line number tracking
2. **Enhanced Timing Calculations**: Improved the Change line calculation using Level 3 with more precise time formatting
3. **Better Error Handling**: Added comprehensive exception handling for message formatting and sending
4. **Dual Page System**: Page 1 now works alongside Page 2, allowing users to toggle between different message formats
5. **Improved Precision**: Enhanced time calculations for more accurate hexagram change predictions

### **Technical Changes**

- **Message Frequency**: Maintained 2-second intervals with improved thread management
- **OSC Protocol**: Enhanced UDP client handling with better connection stability
- **Format Consistency**: Standardized message formatting across all VRChat integrations
- **State Management**: Improved tracking of previous hexagram states for more reliable change detection

The Page 1 format maintains its core structure while adding Level 6 support and improved reliability for VRChat integration.
---

**Version 2.2** represents a significant evolution from 2.0, focusing on stability, performance, and user experience improvements while maintaining all existing functionality.
