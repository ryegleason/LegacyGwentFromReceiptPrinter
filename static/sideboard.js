$(document).ready(function () {

    $(".card").click(function () {
        $(this).toggleClass("selected unselected");
        $("#deck-tab").text("Deck (" + $("#deck .selected").length + ")");
        $("#sideboard-tab").text("Sideboard (" + $("#sideboard .selected").length + ")");
    });

    $("#submitButton").click(function () {
        if ($("#deck .selected").length !== $("#sideboard .selected").length && !window.confirm("The number of cards you're sideboarding out and the number of cards you're brining in are different. Continue?")) {
            return;
        }
        $.post("/sideboard", {
            to_sideboard: $("#deck .selected").map(function () { return this.id; }).get(),
            to_deck: $("#sideboard .selected").map(function () { return this.id; }).get()
        }, function () {
            window.location.href = "/play";
        }, "text");
    });
});