var counter = 0;
const quantity = 20;
var topic = "";
var subtopic = "";


document.addEventListener('DOMContentLoaded', ()=>{
    load();
});

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};


function load() {
    const start = counter;
    const end = start + quantity;
    counter = end;

    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/basics/aphorisms');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            if (res.aphorisms) {
                const aphorisms_template = Handlebars.compile(document.querySelector('#AphorismsHandleBars').innerHTML);
                const aphorisms = aphorisms_template({'aphorisms': res.aphorisms});
                document.querySelector('#allAphorisms').innerHTML += aphorisms;
            }
        } else {
            alert(res.message);
        }
    };

    const data = new FormData();
    data.append('start', start);
    data.append('end', end);
    data.append('topic', topic);
    data.append('subtopic', subtopic);

    request.send(data);
};