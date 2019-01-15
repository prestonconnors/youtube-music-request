$( document ).on( "pagecreate", function() {
    $( "#autocomplete" ).on( "filterablebeforefilter", function ( e, data ) {
        var $ul = $( this ),
            $input = $( data.input ),
            value = $input.val(),
            html = "",
            establishment_id = getCookie("establishment_id")
            extra_search_terms = [];
            mode = "regular";
            if ($("#karaoke-mode :selected").text() == "On") {
                mode = "karaoke";
            }
            $ul.html( "" );
        if ( value && value.length > 2 ) {
            $ul.html( "<li><div class='ui-loader'><span class='ui-icon ui-icon-loading'></span></div></li>" );
            $ul.listview( "refresh" );
            $.ajax({
                url: "/youtube_search/" + $input.val() + extra_search_terms.join(" "),
                dataType: "json",
                crossDomain: true,
                data: {
                }
            })
            .then( function ( response ) {
                $.each( response, function ( i, val ) {
                    var artist = val["title"].split(" - ")[0],
                        title = val["title"].split(" - ")[1];
                    if (val["song_type"] == "karaoke" && mode == "regular") { display_result = 0; }
                    else { display_result = 1; }
                    if (display_result) {
                        if (val["song_type"] == "karaoke") { html += "<li>" + "<a href=\"/request/" + establishment_id + "/" + mode + "/" + val["videoId"] + "\"><img src=\"" + val["thumbnail"] + "\"><p><b>Karaoke Version</b></p>" + artist + "<p>" + title + "</p></a></li>"; }
                        else { html += "<li>" + "<a href=\"/request/" + establishment_id + "/" + mode + "/" + val["videoId"] + "\"><img src=\"" + val["thumbnail"] + "\">" + artist + "<p>" + title + "</p></a></li>"; }
                    }
                    
                });
                $ul.html( html );
                $ul.listview( "refresh" );
                $ul.trigger( "updatelayout");
            });
        }
    });
});

$.mobile.filterable.prototype.options.filterCallback = function( index, searchValue ) {
    return false;
};

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}