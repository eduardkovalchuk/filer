// Call the dataTables jQuery plugin
$('#file_table').dataTable({
  "lengthMenu": [ [25, 50, -1], [25, 50, "всі"] ],
  "searching": false,
  language: {
    "lengthMenu": "Показати _MENU_ на сторінку",
    "zeroRecords": "Пусто",
    "info": "Показано _PAGE_ з _PAGES_",
    "infoEmpty": "Пусто",
    "paginate":{
      "previous":"Попередня",
      "next":"Наступна",
    },
  },
  "columnDefs": [
    { "width": "6%", "targets": 0 },
    { "width": "4%", "targets": -1 }
  ]
});
