document.addEventListener("DOMContentLoaded", ()=>{

    document.querySelector("#register_form").onsubmit = ()=>{
        let name = document.querySelector("#name").value;
        let mobile = document.querySelector("#mobile").value;
        let email = document.querySelector("#email").value;
        let username = document.querySelector("#username").value;
        let password1 = document.querySelector("#password1").value;
        let password2 = document.querySelector("#password2").value;

        if (!email || !password1 || !password2 || !name || !mobile || !username) {
            alert("All fields marked with (*) are required");
            return false;
        }

        
    };

    
});