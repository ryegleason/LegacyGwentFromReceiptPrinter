$(document).ready(function (){
    $(".cardholder img").click(function (){
        if ($(this).data("name")) {
            $("#cardModalTitle").text($(this).data("name"));
            const cardUUID = $(this).data("uuid");

            $("#buyButton").off("click");
            $("#buyButton").click(function (){
                $.post("/move", {
                    uuid: cardUUID,
                    target_zone: "hand",
                    source_zone: "special"
                }, function () {
                    window.location.reload()
                }, "text");
            });

            $("#cardModal").modal("show");
        }
    });
})