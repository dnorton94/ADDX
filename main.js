var columnDefs = [
    {headerName: "Starting Compound", field: "starting", width: 150},
    {headerName: "Final Compound", field: "final", width: 90},
    {headerName: "Reagent", field: "reagent", width: 120},
    {headerName: "Limiting Reagent", field: "limit", width: 90},
    {headerName: "Solvent", field: "solvent", width: 110},
    {headerName: "Temperature", field: "temperature", width: 110},
    // {headerName: "Gold", field: "gold", width: 100},
    // {headerName: "Silver", field: "silver", width: 100},
    // {headerName: "Bronze", field: "bronze", width: 100},
    // {headerName: "Total", field: "total", width: 100}
];

var gridOptions = {
    defaultColDef: {
        editable: true
    },
    columnDefs: columnDefs,
    enableRangeSelection: true,
    rowData: null,
    onRangeSelectionChanged: onRangeSelectionChanged,
    processCellForClipboard: function(params) {
        if (params.column.getColId()==='athlete' && params.value && params.value.toUpperCase) {
            return params.value.toUpperCase();
        } else {
            return params.value;
        }
    },
    processCellFromClipboard: function(params) {
        if (params.column.getColId()==='athlete' && params.value && params.value.toLowerCase) {
            return params.value.toLowerCase();
        } else {
            return params.value;
        }
    }
};

function onAddRange() {
    gridOptions.api.addCellRange({
        rowStartIndex: 4,
        rowEndIndex: 8,
        columnStart: 'age',
        columnEnd: 'date'
    });
}

function onClearRange() {
    gridOptions.api.clearRangeSelection();
}

function onRangeSelectionChanged(event) {

    var lbRangeCount = document.querySelector('#lbRangeCount');
    var lbEagerSum = document.querySelector('#lbEagerSum');
    var lbLazySum = document.querySelector('#lbLazySum');

    var cellRanges = gridOptions.api.getCellRanges();

    // if no selection, clear all the results and do nothing more
    if (!cellRanges || cellRanges.length===0) {
        lbRangeCount.innerHTML = '0';
        lbEagerSum.innerHTML = '-';
        lbLazySum.innerHTML = '-';
        return;
    }

    // set range count to the number of ranges selected
    lbRangeCount.innerHTML = cellRanges.length;

    // consider the first range only. if doing multi select, disregard the others
    var firstRange = cellRanges[0];

    var sum = 0;

    // get starting and ending row, remember rowEnd could be before rowStart
    var startRow = Math.min(firstRange.startRow.rowIndex, firstRange.endRow.rowIndex);
    var endRow = Math.max(firstRange.startRow.rowIndex, firstRange.endRow.rowIndex);

    var api = gridOptions.api;
    for (var rowIndex = startRow; rowIndex<=endRow; rowIndex++) {
        firstRange.columns.forEach( function(column) {
            var rowModel = api.getModel();
            var rowNode = rowModel.getRow(rowIndex);
            var value = api.getValue(column, rowNode);
            if (typeof value === 'number') {
                sum += value;
            }
        });
    }

    lbEagerSum.innerHTML = sum;
    if (event.started) {
        lbLazySum.innerHTML = '?';
    }
    if (event.finished) {
        lbLazySum.innerHTML = sum;
    }
}


var dataOld = [{
    "athlete": "Michael Phelps",
    "age": 23,
    "country": "United States",
    "year": 2008,
    "date": "24/08/2008",
    "sport": "Swimming",
    "gold": 8,
    "silver": 0,
    "bronze": 0,
    "total": 8
},
{
    "athlete": "Michael Phelps",
    "age": 19,
    "country": "United States",
    "year": 2004,
    "date": "29/08/2004",
    "sport": "Swimming",
    "gold": 6,
    "silver": 0,
    "bronze": 2,
    "total": 8
}
]

var data = [{
    "starting": "X",
    "final": "Y",
    "limit": "C02",
    "reagent": "C02",
    "solvent": "acetone",
    "temperature": "90"
},
{
    "starting": "XX",
    "final": "YY",
    "limit": "C02",
    "reagent": "H20",
    "solvent": "acetone",
    "temperature": "90"
}]


// setup the grid after the page has finished loading
document.addEventListener('DOMContentLoaded', function() {
    var gridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(gridDiv, gridOptions);

    gridOptions.api.setRowData(data);


    // // do http request to get our sample data - not using any framework to keep the example self contained.
    // // you will probably use a framework like JQuery, Angular or something else to do your HTTP calls.
    // var httpRequest = new XMLHttpRequest();
    // httpRequest.open('GET', 'https://raw.githubusercontent.com/ag-grid/ag-grid/master/packages/ag-grid-docs/src/olympicWinnersSmall.json');
    // httpRequest.send();
    // httpRequest.onreadystatechange = function() {
    //     if (httpRequest.readyState === 4 && httpRequest.status === 200) {
    //         var httpResult = JSON.parse(httpRequest.responseText);
    //         gridOptions.api.setRowData(httpResult);
    //         gridOptions.api.setRowData(httpResult);
    //     }
    // };
});