### vial-gui

# Docs and getting started

### Please visit [get.vial.today](https://get.vial.today/) to get started with Vial

Vial is an open-source cross-platform (Windows, Linux and Mac) GUI and a QMK fork for configuring your keyboard in real time.


![](https://get.vial.today/img/vial-win-1.png)


---


#### Releases

Visit https://get.vial.today/ to download a binary release of Vial.

#### Development

Requires Python 3.10 or newer.

Install dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To launch the application:

```
source venv/bin/activate
python src/main/python/main.py
```

To produce a frozen build with PyInstaller (platform-specific):

```
pyinstaller vial-mac.spec     # macOS  -> dist/Vial.app
pyinstaller vial-win.spec     # Windows -> dist/Vial/Vial.exe
pyinstaller vial-linux.spec   # Linux   -> dist/Vial/Vial
```
