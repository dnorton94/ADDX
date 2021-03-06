var reagents = [
    "carbonate",
    "sulphuric acid",
    "silver nitrate",
    "potassium nitrate",
    "calcium hypochlorite",
    "potassium dichromate"
];

var temps = [
"10",
"20",
"30",
"40",
"50",
"60"
];

function randomElement(myArray)
{
    return myArray[Math.floor(Math.random() * myArray.length)];
}

function randomReceipe()
{
    var receipe = {
        "starting": "",
        "final": "",
        "limit": "",
        "reagent": "",
        "solvent": "",
        "temperature": ""
    }

    receipe["temp"] = randomElement(temps);

    return receipe;
}

var receipes = [];
var numReceipes = 10;

for (i = 0; i < numReceipes; i++) {
    receipes.push(randomReceipe());
}

var columnDefs = [
    {headerName: "Starting Compound", field: "starting", width: 150},
    {headerName: "Final Compound", field: "final", width: 150},
    {headerName: "Reagent", field: "reagent", width: 150},
    {headerName: "Limiting Reagent", field: "limit", width: 200},
    {headerName: "Solvent", field: "solvent", width: 210},
    {headerName: "Temperature", field: "temperature", width: 210},
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



// setup the grid after the page has finished loading
document.addEventListener('DOMContentLoaded', function() {
    var gridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(gridDiv, gridOptions);

    gridOptions.api.setRowData(receipes);


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