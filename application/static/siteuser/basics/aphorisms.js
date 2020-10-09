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


function ShowAllTopics() {
    if (topic === '') {
        return false;
    }
    counter = 0;
    topic = '';
    subtopic = '';
    document.querySelector('#allAphorisms').innerHTML = '';
    load();
    document.querySelector("#topic_name").innerHTML = "Topics";
    document.querySelector('#SubTopicsDropDown').innerHTML = '';
}



function SelectTopic(tp, stp) {
    if (topic === tp) {
        return false;
    }
    counter = 0;
    topic = tp;
    subtopic = '';
    document.querySelector('#allAphorisms').innerHTML = '';
    load();
    document.querySelector("#topic_name").innerHTML = tp;
    createSubTopicDropDown(stp);
}


function createSubTopicDropDown(stp) {
    const dd_template = Handlebars.compile(document.querySelector('#SubTopicsDropDownHandleBars').innerHTML);
    const dd = dd_template({'subtopics': stp});
    document.querySelector('#SubTopicsDropDown').innerHTML = dd;
}


function SelectSubTopic(stp) {
    if (topic === '' || stp === subtopic) {
        return false;
    }
    counter = 0;
    subtopic = stp;
    document.querySelector('#allAphorisms').innerHTML = '';
    load();
    document.querySelector("#subtopic_name").innerHTML = stp;
}


function ShowAllSubTopics() {
    if (subtopic === '' || topic === '') {
        return false;
    }
    counter = 0;
    subtopic = '';
    document.querySelector('#allAphorisms').innerHTML = '';
    load();
    document.querySelector("#subtopic_name").innerHTML = "SubTopics";
}