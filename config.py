DATE_FORMAT = "%d/%m/%Y"
DATA_PATH = "data_example/fridge_list.csv"

comparator_func = '''(date1, date2) => {
            if (!date1 && !date2) return 0;
            if (!date1) return -1;
            if (!date2) return 1;
            
            const d1 = date1.split('/').reverse().join('');
            const d2 = date2.split('/').reverse().join('');
            
            return d1.localeCompare(d2);
        }'''

# Predefined categories
CATEGORIES = [
    "Fruits",
    "Vegetables", 
    "Dairy",
    "Meat",
    "Fish",
    "Eggs",
    "Bakery",
    "Grains",
    "Beverages",
    "Snacks"
]

COLUMNS_DEFAULTS = [
    {'headerName': 'Item', 'field': 'Item', 'editable': True, 'checkboxSelection': True},
    {
        'headerName': 'Category', 
        'field': 'Category', 
        'editable': True,
        'cellEditor': 'agSelectCellEditor',
        'cellEditorParams': {
            'values': CATEGORIES
        }
    },
    {'headerName': 'Price', 'field': 'Price', 'editable': True, 'type': 'numericColumn'},
    {'headerName': 'Volume/Weight', 'field': 'Volume/Weight', 'editable': True, 'type': 'numericColumn'},
    {
        'headerName': 'Input date', 
        'field': 'Input date', 
        'editable': True,
        ':comparator': comparator_func
    },
    {
        'headerName': 'Expiry date', 
        'field': 'Expiry date', 
        'editable': True,
        ':comparator': comparator_func
    },
]

ROW_SELECTION = "multiple"