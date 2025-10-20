DATE_FORMAT = "%d.%m.%Y"
DATA_PATH = "data/fridge.csv"
DATA_PATH_FREEZER = "data/freezer.csv"
DATA_PATH_CABINET = "data/cabinet.csv"

remove_diacritics_js = '''
function(params) {
    const filterText = params.filterText;
    const cellValue = params.value;
    
    if (cellValue == null) return false;
    
    const removeDiacritics = (str) => {
        return str.normalize('NFD')
                  .replace(/[\u0300-\u036f]/g, '')
                  .toLowerCase();
    };
    
    const normalizedFilter = removeDiacritics(filterText);
    const normalizedCell = removeDiacritics(cellValue);
    
    return normalizedCell.includes(normalizedFilter);
}
'''

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
    {
        'headerName': 'Item',
        'field': 'Item',
        'editable': True,
        'flex': 1,
        'filter': 'agTextColumnFilter',
        'floatingFilter': True,
        'filterParams': {
            ':textMatcher': remove_diacritics_js,
            'buttons': ['reset'],
            'trimInput': True,
            'debounceMs': 300,
        }
    },
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