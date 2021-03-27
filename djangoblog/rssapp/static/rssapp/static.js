const csrftoken = getCookie('csrftoken');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    $("form").submit(function (event) {
        let spinner = document.getElementById("spinner-add");
        spinner.style.display = "block";
        if ("add_feed_form" != $(this).closest('form').attr('id')) {
            return 0
        }
        var formData = {
            title: $("#title").val(),
            body: $("#body").val(),
            url: $("#url").val(),
        };
        var url = $(this).closest('form').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            headers: { 'X-CSRFToken': csrftoken },
            data: formData,
            dataType: "json",
            encode: true,
            statusCode: {
                200: function () {
                    alert("Congrats - your feeds was created!!");
                    spinner.style.display = "none";
                    location.reload();
                },
                400: function (data) {
                    console.log(data)
                    spinner.style.display = "none";
                    alert("Sorry, we can´t save your feed");
                },
                406: function (data) {
                    spinner.style.display = "none";
                    alert("Sorry, we can´t save your feed, " + data.responseJSON["title"][0]);
                },
            },
        }).done(function (data) {
            spinner.style.display = "none";
            console.log(data);
            document.getElementById("add_feed_form").reset();
        });

        event.preventDefault();
    });
});

function deleteFeed(feed) {
    var formData = {
        id: feed.id
    }
    $.ajax({
        type: "DELETE",
        url: "/rss/api",
        headers: { 'X-CSRFToken': csrftoken },
        data: formData,
        dataType: "json",
        encode: true,
        statusCode: {
            200: function () {
                alert("We'd deleted your feed");
                let myobj = document.getElementById(feed.id + '-card');
                myobj.remove();
                //location.reload(); 
            },
            400: function () {
                alert("Sorry, we can´t delete it");
            },
            406: function () {
                alert("Sorry, we can´t delete it");
            },
        },
    }).done(function (data) {
        console.log(data);
    }).fail(function (data) {
        console.log("FAIL...")
    });

}

function addentries(feeds) {
    feeds.forEach(function (feed) {
        let lista = document.getElementById(feed.id + '-list');
        let spinner2 = document.getElementById(feed.id + "-spinner");

        //lista.reset();
        feed.items.forEach(function (item) {
            if (document.getElementById(item.title) == null) {
                let li = document.createElement('li');
                let a = document.createElement('a');
                li.className += "list-group-item";
                a.innerHTML += item.title;
                a.className += "link-secondary";
                a.href = item.url;
                a.id = item.title + item.date;
                a.title = item.description;
                a.target = "_blank";
                li.appendChild(a);
                lista.appendChild(li);
            }
        });
        spinner2.style.display = "none";
    })
}

async function get_entries_from_server(payload) {
    if (document.getElementById("create-card") == null) {
        let spinner = document.getElementById("spinner-home");
        $.ajax({
            type: "POST",
            url: "/rss/api/update/",
            data: payload,
            headers: { 'X-CSRFToken': csrftoken },
            dataType: "json",
            encode: true,
            statusCode: {
                200: function () {
                    console.log("Success");
                    //location.reload();
                },
            },
        }).done(function (data) {
            addentries(data);
            spinner.style.display = "none";
            console.log(data);
        }).fail(function (data) {
            spinner.style.display = "none";
            console.log("FAIL...");
            console.log(data);
        });
    }

}

async function get_feeds() {
    /* "all" = 1 for get all items from 0. 
    Set to 0 to refresh every element by demand */

    var payload = {
        id_feed: 1,
        first: 1,
    }
    get_entries_from_server(payload);

}

function refresh_feeds() {
    let spinner = document.getElementById("spinner-home");
    spinner.style.display = "block";
    get_feeds();
}

async function refresh_by_feed(element) {
    /* "all" = 1 for get all items from 0. 
    Set to 0 to refresh every element by demand */
    id = element.name
    var payload = {
        id_feed: id,
        first: 0,
    }
    get_entries_from_server(payload);
}

window.onload = get_feeds;

/*
How to sen information from server
Id corresponde to the id in user_feed table
feeds = [{'id':45,
    'items':[ {'title':'titulo manual1', 'url':'https://', 'description':'esto es el cuerpo1'},
{'title':'titulo manual2', 'url':'https://', 'description':'esto es el cuerpo2'},
{'title':'titulo manual3', 'url':'https://', 'description':'esto es el cuerpo3'}]}]

*/

