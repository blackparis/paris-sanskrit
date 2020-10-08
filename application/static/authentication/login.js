document.addEventListener("DOMContentLoaded", ()=>{

    document.querySelector("#login_form").onsubmit = ()=>{
        let email = document.querySelector("#email").value;
        let password = document.querySelector("#password").value;

        if (!email || !password) {
            alert("Enter your email address and password.");
            return false;
        }
    };

    
});