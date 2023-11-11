$(document).ready(function () {
    console.log("DATE");

    // Attach the date picker to elements with the 'datepicker' class
    $(".datepicker").datepicker({
        changeYear: true,
        changeMonth: true,
        dateFormat: 'yy-mm-dd' // Use 'dateFormat' instead of 'dateformat'
    });
    
    console.log("NEW DATE SELECTED");
});
