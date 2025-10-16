# iFridge_list

# Installation:
```bash
cd iFridge_list
mkdir data
```

Synchronize the packages and venv:
```
uv sync
```

Create .env>
```bash
nano .env
```
and fill with `USERs` and `STORAGE_SECRET`:

```
USER_admin= password_admin
USER_xxx = password_xxx 
USER_yyy = password_yyy

STORAGE_SECRET= 
````

Compose the docker on

```bash
sudo docker-compose up --build
```

or run 
```python
uv run main.py
```

# 🛠 Project TODOs:
- [x] FIX: sorting of Input Date, Expiry Date
- [x] FEAT: Add columns for PRICE, VOLUME/WEIGHT
- [x] FEAT: Add predefined options for CATEGORIES
- [x] FEAT: Add remove button of selected rows
- [x] FEAT: Add authorization for future accessing through internet
- [x] DOCS: Describe better project in README.md
- [x] REFACTOR: Data Managment of Pandas Data Frame, nested in Class
- [x] REFACTOR: data, data_example, config, config_example
- [x] BUGFIX: datapath in Docker and config example
- [x] REFACTOR: reduce number of columns, remove categories from .csv
- [x] REFACTOR: columns width
- [x] FEAT: add .csv for fridge, cabinet, additional pages
- [ ] FEAT: add possibility to add items as .csv file/dialogue