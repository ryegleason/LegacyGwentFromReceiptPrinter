$(document).ready(function (){
    $("#cardholder img").click(function (){
        $("#cardModalTitle").text($(this).data("name"));
        $("#modalDeckButton").attr("href", "/tuck?uuid=" + $(this).attr("id") + "&source_zone=" + zone_name);
        $("#modalHandButton").attr("href", "/move?uuid=" + $(this).attr("id") + "&target_zone=hand&source_zone=" + zone_name);
        $("#modalPlayButton").attr("href", "/move?uuid=" + $(this).attr("id") + "&target_zone=played&source_zone=" + zone_name);

        $("#cardModal").modal("show");
    });
})