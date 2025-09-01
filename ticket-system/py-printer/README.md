# Costume Ticket Printer Application

A Python GUI application for printing costume rental tickets using thermal printers. This application is built with Tkinter and packaged using PyInstaller for standalone distribution.

## Overview

This application allows users to input customer information and print multiple costume rental tickets. It features:
- Customer name input
- Up to 3 costume entries per customer (number and size)
- Thermal printer integration using USB connection
- Modern GUI with logo display
- Standalone executable via PyInstaller

## PyInstaller Issues and Fixes

During the packaging process with PyInstaller, several issues were encountered and resolved:

### Issue 1: Missing `escpos/capabilities.json` File

**Problem:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/path/to/dist/app/_internal/escpos/capabilities.json'
```

**Cause:**
PyInstaller didn't automatically include the `capabilities.json` data file required by the `python-escpos` library. This file contains printer capability definitions that the library needs to function properly.

**Solution:**
Updated the `app.spec` file to explicitly include the data file:
```python
datas=[('env/lib/python3.10/site-packages/escpos/capabilities.json', 'escpos/'), ...]
```

### Issue 2: Image File Path Resolution

**Problem:**
```
FileNotFoundError: [Errno 2] No such file or directory: './pc-logo.png'
```

**Cause:**
In PyInstaller bundles, relative paths don't work the same way as in development environments. The application couldn't locate the logo images.

**Solutions:**
1. **Added image files to PyInstaller bundle:**
   ```python
   datas=[..., ('logo.png', '.'), ('pc-logo.png', '.')]
   ```

2. **Created a resource path helper function in `app.py`:**
   ```python
   def resource_path(relative_path):
       """ Get absolute path to resource, works for dev and for PyInstaller """
       try:
           # PyInstaller creates a temp folder and stores path in _MEIPASS
           base_path = sys._MEIPASS
       except Exception:
           base_path = os.path.abspath(".")
       
       return os.path.join(base_path, relative_path)
   ```

3. **Updated image loading to use the helper function:**
   ```python
   logo_image = Image.open(resource_path("pc-logo.png"))
   ```

### Issue 3: PIL/Tkinter Integration

**Problem:**
```
ModuleNotFoundError: No module named 'PIL._tkinter_finder'
_tkinter.TclError: invalid command name "PyImagingPhoto"
```

**Cause:**
PyInstaller failed to detect and include necessary PIL (Pillow) modules required for tkinter integration, specifically for displaying images in tkinter widgets.

**Solution:**
Added missing modules to hidden imports in `app.spec`:
```python
hiddenimports=[
    'escpos', 'escpos.printer', 'escpos.printer.usb', 
    'usb.core', 'usb.util', 
    'PIL._tkinter_finder', 'PIL._imagingtk'
]
```

## Final app.spec Configuration

The complete working `app.spec` file includes:

```python
a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('env/lib/python3.10/site-packages/escpos/capabilities.json', 'escpos/'), 
        ('logo.png', '.'), 
        ('pc-logo.png', '.')
    ],
    hiddenimports=[
        'escpos', 'escpos.printer', 'escpos.printer.usb', 
        'usb.core', 'usb.util', 
        'PIL._tkinter_finder', 'PIL._imagingtk'
    ],
    # ... other configurations
)
```

## Dependencies

The application requires the following Python packages (see `requirements.txt`):
- `python-escpos==3.1` - Thermal printer communication
- `pillow==11.2.1` - Image processing
- `pyusb==1.3.1` - USB device communication
- `pyinstaller==6.14.2` - Application packaging
- `tkinter` (included with Python) - GUI framework

## Hardware Requirements

- USB thermal printer (configured for vendor_id=0x076c, product_id=0x0302)
- USB connection to the printer

## Building the Application

To build the standalone executable:

1. **Activate the virtual environment:**
   ```bash
   source env/bin/activate
   ```

2. **Build with PyInstaller:**
   ```bash
   pyinstaller app.spec --clean --noconfirm
   ```

3. **The executable will be created in:**
   ```
   dist/app/app
   ```

## Running the Application

### Development Mode
```bash
python app.py
```

### Standalone Executable
```bash
cd dist/app
./app
```

## Application Distribution

The PyInstaller build creates a self-contained application that can be distributed to end users without requiring them to install Python or any dependencies.

### Distribution Package Contents

After building with PyInstaller, the `dist/app/` directory contains everything needed to run the application:

```
dist/app/
├── app                 # Main executable file
└── _internal/          # Supporting libraries and data files
    ├── escpos/
    │   └── capabilities.json
    ├── logo.png
    ├── pc-logo.png
    └── [various Python libraries and dependencies]
```

### Distribution Methods

#### Method 1: Direct Directory Copy
1. **Copy the entire `dist/app/` directory** to the target system
2. **Ensure the directory structure remains intact** - the `_internal/` folder must stay alongside the `app` executable
3. **Set execute permissions** (Linux/macOS):
   ```bash
   chmod +x app
   ```

#### Method 2: Archive Distribution
1. **Create a compressed archive:**
   ```bash
   cd dist
   tar -czf costume-printer-app.tar.gz app/
   # or
   zip -r costume-printer-app.zip app/
   ```

2. **Extract on target system:**
   ```bash
   tar -xzf costume-printer-app.tar.gz
   # or
   unzip costume-printer-app.zip
   ```

#### Method 3: Installer Creation (Advanced)
For more professional distribution, consider creating installers:
- **Linux**: Use tools like `makeself` or `fpm`
- **Windows**: Use NSIS, Inno Setup, or WiX
- **macOS**: Create `.dmg` files or use `pkgbuild`

### System Requirements for End Users

#### Minimum Requirements
- **Operating System**: Linux (64-bit) - built for the target system architecture
- **USB Support**: For thermal printer connectivity
- **Display**: GUI environment (X11/Wayland for Linux)

#### Hardware Requirements
- **USB thermal printer** compatible with the configured vendor/product IDs
- **USB port** for printer connection
- **Minimum RAM**: 100MB available memory
- **Disk Space**: ~50MB for the application

### Installation Instructions for End Users

1. **Download and extract** the application package
2. **Connect the thermal printer** via USB
3. **Set printer permissions** (if needed):
   ```bash
   # Add user to dialout group for USB access
   sudo usermod -a -G dialout $USER
   # Then log out and log back in
   ```
4. **Run the application:**
   ```bash
   cd costume-printer-app/app
   ./app
   ```

### Deployment Considerations

#### Security
- The application runs with user privileges (no root access required for basic operation)
- USB device access may require group membership or udev rules
- Consider code signing for trusted distribution

#### Updates
- **Full replacement**: Distribute new versions by replacing the entire app directory
- **Version checking**: Consider implementing version checks within the application
- **Backup settings**: If adding configuration files, document backup procedures

#### Multi-Platform Distribution
- **Separate builds required** for different operating systems and architectures
- **Build naming convention**: Use descriptive names like:
  - `costume-printer-linux-x64-v1.0.tar.gz`
  - `costume-printer-windows-x64-v1.0.zip`
  - `costume-printer-macos-x64-v1.0.dmg`

#### USB Printer Setup
End users may need to:
1. **Install printer drivers** (if not using generic thermal printer drivers)
2. **Configure printer settings** in the system
3. **Test printer connectivity** before running the application
4. **Check vendor_id and product_id** match their specific printer model

### Distribution Checklist

Before distributing the application:

- [ ] Test the executable on a clean system without Python installed
- [ ] Verify all image files and data files are included
- [ ] Test printer functionality on target hardware
- [ ] Document any required system configuration
- [ ] Include troubleshooting instructions
- [ ] Test USB permissions and access
- [ ] Verify the application works without internet connectivity
- [ ] Check file permissions are correctly set

## Troubleshooting

### Common PyInstaller Issues

1. **Missing Data Files:**
   - Check that all required data files are listed in the `datas` section of `app.spec`
   - Use `find . -name "*.json" -o -name "*.png"` in the dist directory to verify files are included

2. **Missing Modules:**
   - Add any missing modules to the `hiddenimports` list in `app.spec`
   - Use `--debug=imports` flag with PyInstaller to see import issues

3. **Path Resolution:**
   - Always use the `resource_path()` function for accessing bundled files
   - Test both development and packaged versions

### Printer Issues

1. **USB Permissions:**
   - Ensure the user has permission to access USB devices
   - May require adding user to appropriate groups or running with sudo

2. **Printer Configuration:**
   - Verify vendor_id and product_id match your printer
   - Check USB connection and printer power

## File Structure

```
test-printer/
├── app.py              # Main GUI application
├── print.py            # Printer interface module
├── app.spec            # PyInstaller specification
├── requirements.txt    # Python dependencies
├── pc-logo.png         # Application logo
├── logo.png           # Additional logo
├── README.md          # This file
├── env/               # Virtual environment
├── build/             # PyInstaller build files
└── dist/              # Final executable output
    └── app/
        ├── app        # Standalone executable
        └── _internal/ # Supporting files and libraries
```

## Development Notes

- The application uses a virtual environment (`env/`) to manage dependencies
- PyInstaller creates a `_MEIPASS` temporary directory when running the executable
- The `resource_path()` function handles the difference between development and packaged environments
- All printer communication is handled through the `print.py` module
- The GUI supports up to 3 costume entries per customer transaction

## Version History

- **v1.0** - Initial working version with PyInstaller fixes
  - Fixed escpos capabilities.json inclusion
  - Fixed image path resolution
  - Fixed PIL/tkinter integration
  - Added proper resource path handling
