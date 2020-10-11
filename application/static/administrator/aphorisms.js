document.addEventListener("DOMContentLoaded", ()=>{

    document.querySelector("#add_topic_link").onclick = ()=>{
        document.querySelector("#add_topic_form").style.display = "block";
        document.querySelector("#topic_name").value = '';
        document.querySelector("#topic_name").focus();
        document.querySelector("#add_topic_error").innerHTML = '';
        return false;
    };

    document.querySelector("#cancel_add_topic").onclick = ()=>{
        document.querySelector("#add_topic_error").innerHTML = '';
        document.querySelector("#add_topic_form").style.display = "none";
        return false;
    };

    document.querySelector("#add_topic").onsubmit = ()=>{
        let topic_name = document.querySelector("#topic_name").value;
        if (!topic_name) {
            document.querySelector("#cancel_add_topic").click();
            return false;
        }

        var meta = document.getElementsByTagName("meta")[0];
        var csrftoken = meta.content;
        const request = new XMLHttpRequest();
        request.open('POST', '/administrator/add_topic');
        request.setRequestHeader("X-CSRFToken", csrftoken);   

        request.onload = () => {
            const res = JSON.parse(request.responseText);
            if (res.success) {
                const topic_div = Handlebars.compile(document.querySelector('#TopicDivHandleBars').innerHTML);
                const topic = topic_div({'topic_id': res.topic_id, "topic_name": res.topic_name});
                document.querySelector('#topics_list').innerHTML += topic;
                document.querySelector("#add_topic_form").style.display = "none";
            } else {
                document.querySelector("#add_topic_error").innerHTML = res.message;
            }
        };

        const data = new FormData();
        data.append('topic_name', topic_name);
        request.send(data);
        return false;
    };
});


function SelectTopic(topic_id) {
    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/administrator/get_subtopic');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            const subtopic_template = Handlebars.compile(document.querySelector('#SubTopicDivHandleBars').innerHTML);
            const subtopic_div = subtopic_template({'topic_id': res.topic_id, "subtopics": res.subtopics, "topic_name": res.topic_name});
            document.querySelector("#subtopics_div").innerHTML = subtopic_div;
            document.querySelector('#aphorisms_div').innerHTML = "";
        } else {
            alert(res.message);
        }
    };

    const data = new FormData();
    data.append('topic_id', topic_id);
    request.send(data);
    return false;
}


function AddSubTopic(topic_id) {
    let subtopic_name = document.querySelector("#subtopic_name").value;
    if (!subtopic_name) {
        cancel_add_subtopic();
        return false;
    }

    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/administrator/add_subtopic');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            const stopic_div = Handlebars.compile(document.querySelector('#SubTopicHandleBars').innerHTML);
            const stopic = stopic_div({'subtopic_id': res.subtopic_id, "subtopic_name": res.subtopic_name, "topic_id": res.topic_id});
            document.querySelector('#subtopics_list').innerHTML += stopic;
            cancel_add_subtopic();
        } else {
            document.querySelector("#add_subtopic_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('topic_id', topic_id);
    data.append('subtopic_name', subtopic_name);
    request.send(data);
    return false;
}


function add_subtopic_link() {
    document.querySelector("#add_subtopic_form").style.display = "block";
    document.querySelector("#subtopic_name").value = '';
    document.querySelector("#subtopic_name").focus();
    document.querySelector("#add_subtopic_error").innerHTML = '';
    return false;
}


function add_rule_link() {
    document.querySelector("#add_rule_form").style.display = "block";
    document.querySelector("#aphorism_number").value = '';
    document.querySelector("#aphorism").value = '';
    document.querySelector("#aphorism_number").focus();
    document.querySelector("#add_rule_error").innerHTML = '';
    return false;
}


function cancel_add_subtopic() {
    document.querySelector("#add_subtopic_error").innerHTML = '';
    document.querySelector("#add_subtopic_form").style.display = "none";
    return false;
}


function cancel_add_rule() {
    document.querySelector("#add_rule_error").innerHTML = '';
    document.querySelector("#add_rule_form").style.display = "none";
    return false;
}


function SelectSubTopic(subtopic_id) {

    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/administrator/get_rules');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            const rules_template = Handlebars.compile(document.querySelector('#RulesDivHandleBars').innerHTML);
            const rules_div = rules_template({
                "topic_name": res.topic_name,
                "subtopic_name": res.subtopic_name,
                "subtopic_id": res.subtopic_id,
                "aphorisms": res.aphorisms
            });
            document.querySelector('#aphorisms_div').innerHTML = rules_div;
        } else {
            alert(res.message);
        }
    };

    const data = new FormData();
    data.append('subtopic_id', subtopic_id);
    request.send(data);
    return false;
}


function AddRule(subtopic_id) {
    let number = document.querySelector("#aphorism_number").value;
    let aphorism = document.querySelector("#aphorism").value;

    if (!number || !aphorism) {
        cancel_add_rule();
        return false;
    }

    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/administrator/add_aphorism');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            const r_div = Handlebars.compile(document.querySelector('#RulesHandleBars').innerHTML);
            const r = r_div({
                "rule_id": res.rule_id,
                "number": res.number,
                "rule": res.rule,
                "subtopic_id": subtopic_id
            });
            document.querySelector('#rules_list').innerHTML += r;
            cancel_add_rule();
        } else {
            document.querySelector("#add_rule_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('subtopic_id', subtopic_id);
    data.append('number', number);
    data.append('aphorism', aphorism);
    request.send(data);
    return false;
}


function CloseEditingForms() {
    document.querySelectorAll(".editing").forEach(d=>{
        d.innerHTML = '';
    });
    document.querySelectorAll(".errorMessage").forEach(d=>{
        d.innerHTML = '';
    });
}


function edit_topic(topic_id, topic_name) {
    CloseEditingForms();
    const EditTopicFormTemplate = Handlebars.compile(document.querySelector('#EditTopicFormHandleBars').innerHTML);
    const EditTopicForm = EditTopicFormTemplate({
        "topic_id": topic_id,
        "topic_name": topic_name,
    });
    document.querySelector(`#edit_topic_form_${topic_id}`).innerHTML = EditTopicForm;
    document.querySelector(`#topic_name_${topic_id}`).focus();
}


function EditTopic(topic_id, topic_name) {
    let TopicName = document.querySelector(`#topic_name_${topic_id}`).value;
    if (!TopicName || TopicName === topic_name) {
        CloseEditingForms();
        return false;
    }

    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/administrator/edit_topic');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            location.reload();
        } else {
            document.querySelector("#edit_topic_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('topic_id', topic_id);
    data.append('TopicName', TopicName);
    request.send(data);
    return false;
}


function edit_subtopic(subtopic_id, subtopic_name, topic_id) {
    CloseEditingForms();

    const request = new XMLHttpRequest();
    request.open('GET', '/administrator/get_topics');

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            const EditSubTopicFormTemplate = Handlebars.compile(document.querySelector('#EditSubTopicFormHandleBars').innerHTML);
            const EditSubTopicForm = EditSubTopicFormTemplate({
                "subtopic_id": subtopic_id,
                "subtopic_name": subtopic_name,
                "topic_id": topic_id,
                "topics": res.topics
            });
            document.querySelector(`#edit_subtopic_form_${subtopic_id}`).innerHTML = EditSubTopicForm;
            document.querySelector(`#subtopic_name_${subtopic_id}`).focus();
            document.querySelector(`#selectTopics_${topic_id}`).value = topic_id;
        } else {
            alert(res.message);
        }
    };

    request.send();
    return false;
}


function EditSubTopic(subtopic_id, subtopic_name, topic_id) {
    let SubTopicName = document.querySelector(`#subtopic_name_${subtopic_id}`).value;
    let new_topic_id = document.querySelector(`#selectTopics_${topic_id}`).value;
    if (!SubTopicName || (SubTopicName === subtopic_name && topic_id === new_topic_id)) {
        CloseEditingForms();
        return false;
    }

    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/administrator/edit_subtopic');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            location.reload();
        } else {
            document.querySelector("#edit_subtopic_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('subtopic_id', subtopic_id);
    data.append('SubTopicName', SubTopicName);
    data.append('topic_id', topic_id);
    data.append('new_topic_id', new_topic_id);
    request.send(data);
    return false;
}


function edit_rule(rule_number, rule, rule_id, subtopic_id) {
    CloseEditingForms();

    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/administrator/GetSubTopics');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            const EditRuleFormTemplate = Handlebars.compile(document.querySelector('#EditRuleFormHandleBars').innerHTML);
            const EditRuleForm = EditRuleFormTemplate({
                "rule_id": rule_id,
                "subtopics": res.subtopics,
                "rule_number": rule_number,
                "rule": rule,
                "subtopic_id": subtopic_id
            });
            document.querySelector(`#edit_rule_form_${rule_id}`).innerHTML = EditRuleForm;
            document.querySelector(`#aphorism_number_${rule_id}`).focus();
            document.querySelector(`#selectSubTopics_${rule_id}`).value = subtopic_id;
        } else {
            alert(res.message);
        }
    };

    const data = new FormData();
    data.append('subtopic_id', subtopic_id);
    request.send(data);
    return false;
}


function EditRule(rule_id, subtopic_id, rule_number, rule) {
    let new_subtopic_id = document.querySelector(`#selectSubTopics_${rule_id}`).value;
    let new_rule_number = document.querySelector(`#aphorism_number_${rule_id}`).value;
    let new_rule = document.querySelector(`#aphorism_${rule_id}`).value;

    if (!new_subtopic_id || !new_rule_number || !new_rule) {
        CloseEditingForms();
        return false;
    }

    if (new_subtopic_id === subtopic_id && new_rule_number === rule_number && new_rule === rule) {
        CloseEditingForms();
        return false;
    }

    var meta = document.getElementsByTagName("meta")[0];
    var csrftoken = meta.content;
    const request = new XMLHttpRequest();
    request.open('POST', '/administrator/edit_rule');
    request.setRequestHeader("X-CSRFToken", csrftoken);   

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            location.reload();
        } else {
            document.querySelector("#edit_rule_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('new_subtopic_id', new_subtopic_id);
    data.append('new_rule_number', new_rule_number);
    data.append('new_rule', new_rule);
    data.append('rule_id', rule_id);
    request.send(data);
    return false;
}