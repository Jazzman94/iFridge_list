DATE_FORMAT = "%d.%m.%Y"
DATA_PATH = "data/fridge.csv"
DATA_PATH_FREEZER = "data/freezer.csv"
DATA_PATH_CABINET = "data/cabinet.csv"

comparator_func = '''(date1, date2) => {
            if (!date1 && !date2) return 0;
            if (!date1) return -1;
            if (!date2) return 1;

            const d1 = date1.split('.').reverse().join('');
            const d2 = date2.split('.').reverse().join('');

            return d1.localeCompare(d2);
        }'''

COLUMNS_DEFAULTS = [
    {'headerName': 'id', 'field': 'id', 'checkboxSelection': True, 'width': 40},
    {'headerName': 'Item', 'field': 'Item', 'editable': True, 'flex': 1},
    {'headerName': 'Quantity', 'field': 'Quantity', 'editable': True, 'type': 'numericColumn', 'width': 50},
    {
        'headerName': 'Expiry date', 
        'field': 'Expiry date', 
        'editable': True,
        ':comparator': comparator_func,
        'width': 100,
    },
]


ROW_SELECTION = "multiple"