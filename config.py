DATE_FORMAT = "%d.%m.%Y"
DATA_PATH = "data_example/example.csv"

comparator_func = '''(date1, date2) => {
            if (!date1 && !date2) return 0;
            if (!date1) return -1;
            if (!date2) return 1;

            const d1 = date1.split('.').reverse().join('');
            const d2 = date2.split('.').reverse().join('');

            return d1.localeCompare(d2);
        }'''

# Predefined categories
CATEGORIES = [
    "Fruits",
    "Vegetables", 
    "Dairy",
    "Meat",
    "Fish",
    "Fish",
    "Eggs",
    "Bakery",
    "Grains",
    "Beverages",
    "Snacks"
]

COLUMNS_DEFAULTS = [
    {'headerName': 'id', 'field': 'id', 'hide': True},
    {'headerName': 'Item', 'field': 'Item', 'editable': True, 'checkboxSelection': True},
    {'headerName': 'Quantity', 'field': 'Quantity', 'editable': True, 'type': 'numericColumn'},
    {
        'headerName': 'Expiry date', 
        'field': 'Expiry date', 
        'editable': True,
        ':comparator': comparator_func,
    },
]

ROW_SELECTION = "multiple"