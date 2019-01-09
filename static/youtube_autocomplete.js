$( document ).on( "pagecreate", function() {
    $( "#autocomplete" ).on( "filterablebeforefilter", function ( e, data ) {
        var $ul = $( this ),
            $input = $( data.input ),
            value = $input.val(),
            html = "",
            establishment_id = getCookie("establishment_id")
            extra_search_terms = [];
            if (document.getElementById("karaoke").value == "true") {
                extra_search_terms.push("karaoke");
            }
            if (extra_search_terms.length > 0) {
                extra_search_terms.unshift("");
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
                    html += "<li>" + "<a href=\"/request/" + establishment_id + "/" + val["videoId"] + "\"><img src=\"" + val["thumbnail"] + "\">" + artist + "<p>" + title + "</p></a></li>";
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