function menu(x) {
    x.classList.toggle("change");
    var y = document.getElementById("links");
    if (y.style.display === "block") {
        y.style.display = "none";
    } else {
        y.classList.toggle("smooth_link");
    }
}
function Reguserchange(list){
    var s = document.getElementsByClassName("stu");
    var t = document.getElementsByClassName("teach");
    var value = list.options[list.selectedIndex].value;
    if(value==0){
        for(let i=0;i<t.length;i++){
            t[i].style.display="none";
        }
        for(let i=0;i<s.length;i++){
            s[i].style.display="none";
        }
    }
    else if(value==1){
        for(let i=0;i<s.length;i++){
            s[i].style.display="block";
        }
        for(let i=0;i<t.length;i++){
            t[i].style.display="none";
        }
    }
    else if(value==2){
        for(let i=0;i<t.length;i++){
            t[i].style.display="block";
        }
        for(let i=0;i<s.length;i++){
            s[i].style.display="none";
        }
    }
}
function validateregForm() {
    let name = document.getElementById("Myregname").value;
    let email = document.forms["Regform"]["email"].value;
    let pass = document.getElementById("Myregpass").value;
    let confpass = document.getElementById("Myregconfpass").value;
    let Myclass = document.getElementById("Myregclass");
    let Mytype = document.getElementById("Myregtype")
    let phone = document.getElementById("Myregphone").value;
    let add = document.getElementById("Myregadd").value;
    let exp = document.getElementById("Myregexp").value;
    let sub = document.getElementById("Myregsub");
    let d1 = document.getElementById("regalert1");
    d1.innerHTML = "";
    if (name == "") {
        d1.innerHTML = "Please enter name.";
        return false;
    }
    if(isNaN(name)==false){
        d1.innerHTML = "Invalid name";
        return false;
    }
    if (email == "") {
        d1.innerHTML = "Please enter email.";
        return false;
    }
    if (pass == "") {
        d1.innerHTML = "Please enter Password.";
        return false;
    }
    if (confpass == "") {
        d1.innerHTML = "Please enter confirm Password. ";
        return false;
    }
    if(pass.length < 6){
        d1.innerHTML = "Password length must be greater than 8.";
        return false;
    }
    if(pass != confpass){
        d1.innerHTML = "Password is not same.";
        return false;
    }
  
    if (Mytype.options[Mytype.selectedIndex].value == 0 ) {
        d1.innerHTML = "Please enter type.";    
        return false;
    }
    if (Mytype.options[Mytype.selectedIndex].value == 1 ) {
        if(add==""){
            d1.innerHTML = "Please Enter Address.";
            return false;
        }   
    }
    if (Mytype.options[Mytype.selectedIndex].value == 1 ) {
        if (Myclass.options[Myclass.selectedIndex].value == 0 ) {
            d1.innerHTML = "Please enter Class.";    
            return false;
        }
    }
    if (Mytype.options[Mytype.selectedIndex].value == 2 ) {
        if (exp == "") {
            d1.innerHTML = "Please enter Experience";
            return false;
        }
        if(isNaN(exp) == true){
            d1.innerHTML = "Invalid Experience";
            return false;
        } 
        if (sub.options[sub.selectedIndex].value == 0 ) {
            d1.innerHTML = "Please enter subject";    
            return false;
        }
    }
    if (phone == "") {
        d1.innerHTML = "Please enter Phone no.";
        return false;
    }
    if(isNaN(phone) == true){
        d1.innerHTML ="Invalid Phone no.";
        return false;
    }
    var t = document.getElementsByClassName("regalert");
    for(let i=0;i<t.length;i++){
        t[i].style.display="block";
    }

}
function ResetregForm() {
    var s = document.getElementsByClassName("stu");
    var t = document.getElementsByClassName("teach");
    for(let i=0;i<t.length;i++){
        t[i].style.display="none";
    }
    for(let i=0;i<s.length;i++){
        s[i].style.display="none";
    }
}