# Teilnehmendenverwaltung
*by [BinaNoir](https://github.com/BinaNoir), [EvelineFlowercrown](https://github.com/EvelineFlowercrown) and [grimmchristoph84](https://github.com/grimmchristoph84-commits)*

## Description
This database is used to manage participants in a rehabilitation program. 
See example version with mock data: https://teilnehmerverwaltung.onrender.com/

## Installation
1. Download Python 3.3.17 (or later) from https://www.python.org/ and install it.
2. Open your terminal:<br>
Linux: `[strg] + [alt] + [t]`<br>
Windows: `[win] + [X]` → `wt` → `[Enter]`
3. Clone this repository:   
```bash
git clone https://github.com/EvelineFlowercrown/TeilnehmerVerwaltung.git
```
4. Install the required packages from requirements.txt :
```bash
pip install -r requirements.txt
```

## Testing
Change to the main directory.
```bash
cd ~/<path>/TeilnehmerVerwaltung
```

Run all tests: 
```bash
python -m pytest
```
Test a specific module: 
```bash
python -m pytest tests/<modul>
```
Test a specific function in a modul:
```bash
python -m pytest tests/<modul>/::<test_function>
```
