function initDataTables() {
    $('#table-establecimientos').DataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.10.22/i18n/Spanish.json"
        },
        paging: false,
        pageLength: 3,
        lengthChange: false,
        info: false,
        columnDefs: [
            { type: "html", targets: [0, 3] },
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
        columnDefs: [
            { type: "html", targets: [1] },
            { orderable: false, targets: [1, -1] },
            { searchable: false, targets: -1 }
        ]
    });
}

initDataTables();