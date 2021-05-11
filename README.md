# SakiSimulatorGUI
This project is originated from the [사키 시뮬레이터](https://cafe.naver.com/rookieonline/102524).

## How to run
Double click `dist/main/main.exe` file.

## How to compile
Used [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) to compile with below options

 - `One directory` Option
 - `Console mode` Option
 - Additional files:
   - `src/__init__.py`
   - `src/main_page.py`
   - `src/spirit_page.py`
   - `src/userdata_template.py`
   - `src/utils.py`
   - `src/weapon_page.py`
   - `data/`
 - Advanced:
   - debug: all

For production, it'll be improved to use
 - `One file` Option
 - `Windowed mode` Option
 - Advance:
   - debug: None