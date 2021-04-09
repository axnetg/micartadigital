function initDataTables() {
    $('#table-establecimientos').DataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.10.22/i18n/Spanish.json"
        },
        paging: false,
        pageLength: 3,
        lengthChange: false,
        info: false,
        autoWidth: false,
        columnDefs: [
            { type: "html", targets: [0, 3] },
            { width: "50%", targets: 0 },
            { orderable: false, targets: -1 },
            { searchable: false, targets: -1 }
        ]
    });

    $('#table-cartas').DataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.10.22/i18n/Spanish.json"
        },
        paging: false,
        pageLength: 3,
        lengthChange: false,
        info: false,
        autoWidth: false,
        columnDefs: [
            { type: "html", targets: [0, 1] },
            { width: "25%", targets: 0 },
            { orderable: false, targets: [1, -1] },
            { searchable: false, targets: -1 }
        ]
    });
}

initDataTables();