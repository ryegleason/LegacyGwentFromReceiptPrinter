$(document).ready(function (){
    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function(e) {
        localStorage.setItem('activeTab', $(e.target).data('bs-target'));
    });
    var activeTab = localStorage.getItem('activeTab');
    if(activeTab){
        $('#mainTabs button[data-bs-target="' + activeTab + '"]').tab('show');
    }

    const cardModalTitle = $("#cardModalTitle");
    const modalButton1 = $("#modalButton1");
    const modalButton2 = $("#modalButton2");

    function deckOnClick(event) {
        console.log("deckOnClick");
        cardModalTitle.text($(this).data("name"));
        modalButton1.text("Put in hand");
        modalButton2.text("Play");
        modalButton1.off("click");
        modalButton2.off("click");
        modalButton1.click(function () {
            $.post("/move", {
                uuid: event.target.id,
                source_zone: "deck",
                target_zone: "hand"
            }, function () {
                $("#hand .cardholder").append(event.target);
                $(event.target).off("click");
                $(event.target).click(handOnClick);
            }, "text");
        });

        modalButton2.click(function () {
            $.post("/move", {
                uuid: event.target.id,
                source_zone: "deck",
                target_zone: "played"
            }, function () {
                $("#played .cardholder").append(event.target);
                $(event.target).off("click");
                $(event.target).click(playedOnClick);
            }, "text");
        });
        $("#cardModal").modal("show");
    }

    function handOnClick(event) {
        console.log("handOnClick");
        cardModalTitle.text($(this).data("name"));
        modalButton1.text("Put in deck");
        modalButton2.text("Play");
        modalButton1.off("click");
        modalButton2.off("click");
        modalButton1.click(function () {
            window.location.href = "/tuck?uuid=" + event.target.id + "&source_zone=hand";
        });
        modalButton2.click(function () {
            $.post("/move", {
                uuid: event.target.id,
                source_zone: "hand",
                target_zone: "played"
            }, function () {
                $("#played .cardholder").append(event.target);
                $(event.target).off("click");
                $(event.target).click(playedOnClick);
            }, "text");
        });
        $("#cardModal").modal("show");
    }

    function playedOnClick(event) {
        console.log("playedOnClick");
        cardModalTitle.text($(this).data("name"));
        modalButton1.text("Put in deck");
        modalButton2.text("Put in hand");
        modalButton1.off("click");
        modalButton2.off("click");
        modalButton1.click(function () {
            window.location.href = "/tuck?uuid=" + event.target.id + "&source_zone=played";
        });

        modalButton2.click(function () {
            $.post("/move", {
                uuid: event.target.id,
                source_zone: "played",
                target_zone: "hand"
            }, function () {
                $("#hand .cardholder").append(event.target);
                $(event.target).off("click");
                $(event.target).click(handOnClick);
            }, "text");
        });
        $("#cardModal").modal("show");
    }

    $("#deck .card").click(deckOnClick);

    $("#hand .card").click(handOnClick);

    $("#played .card").click(playedOnClick);

    $("#shuffleButton").click(function () {
        $.post("/shuffle", {}, null, "text");
    });

    $("#drawButton").click(function () {
        $.post("/draw", {draw_to: "hand"}, function (response) {
            if (response["uuid"] != null) {
                const card = document.getElementById(response["uuid"]);
                $("#hand .cardholder").append(card);
                $(card).off("click");
                $(card).click(handOnClick);
            }
            for (const cardData of response["new_cards"]) {
                const card = document.createElement("img");
                card.src = cardData["image_url"];
                card.id = cardData["uuid"];
                card.className = "card";
                card.dataset.name = cardData["name"];
                if (cardData["zone"] === "deck") {
                    $("#deck .cardholder").append(card);
                    $(card).click(deckOnClick);
                } else if (cardData["zone"] === "hand") {
                    $("#hand .cardholder").append(card);
                    $(card).click(handOnClick);
                } else if (cardData["zone"] === "played") {
                    $("#played .cardholder").append(card);
                    $(card).click(playedOnClick);
                } else {
                    console.log("Unknown zone: " + cardData["zone"] + " for new card: " + cardData["name"]);
                }
            }
        }, "json");
    });
});