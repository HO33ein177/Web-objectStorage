//  وقتی که رمزی داخل فیلد رمز وارد شد عکس چشم در سمت راست ظاهر شود و وقتی برداشته شدچشم حذف میشود
document.getElementById('inputp1').addEventListener('input',function(){
    const pasfild = document.getElementById('inputp1');
    const image = document.getElementById("hide1");
    if(!pasfild.value){
        image.style.display = 'none';
    }else{
        image.style.display = 'block';
    }
});

//  وقتی روی چشم زدیم رمز رویت شود و یا مخفی شود
document.getElementById('hide1').addEventListener('click',function(){
    const pasfild = document.getElementById('inputp1');
    if(pasfild.type == "password"){
        pasfild.type = "text";
    }
    else{
        pasfild.type = "password";
    }   
    
});

//  وقتی که رمزی داخل فیلد رمز وارد شد عکس چشم در سمت راست ظاهر شود و وقتی برداشته شدچشم حذف میشود
document.getElementById('inputp2').addEventListener('input',function(){
    const pasfild = document.getElementById('inputp2');
    const image = document.getElementById("hide2");
    if(!pasfild.value){
        image.style.display = 'none';
    }else{
        image.style.display = 'block';
    }
});

//  وقتی روی چشم زدیم رمز رویت شود و یا مخفی شود
document.getElementById('hide2').addEventListener('click',function(){
    const pasfild = document.getElementById('inputp2');
    if(pasfild.type == "password"){
        pasfild.type = "text";
    }
    else{
        pasfild.type = "password";
    }   
});


// وقتی روی دکمه سابمیت زده شد اگر رمزها تطابق نداشت هشدار میدهد
function submit(){
    const passwordField = document.getElementById('inputp1');
    const confirmPasswordField = document.getElementById('inputp2');
    const box = document.getElementById('fields1');
    const allert = document.getElementById('hoshdar');

    if (confirmPasswordField.value !== passwordField.value) {
        box.style.border = 'solid 0.5px #ff0000 ';
        allert.style.display= 'block';
    } else {
        box.style.border = 'none';
        allert.style.display= 'none';
    }
}

//  وقتی که رمزی داخل فیلد رمز وارد شد عکس چشم در سمت راست ظاهر شود و وقتی برداشته شدچشم حذف میشود
document.getElementById('inputPL').addEventListener('input',function(){
    const pasfild = document.getElementById('inputPL');
    const image = document.getElementById("hide3");
    if(!pasfild.value){
        image.style.display = 'none';
    }else{
        image.style.display = 'block';
    }
});

//  وقتی روی چشم زدیم رمز رویت شود و یا مخفی شود
document.getElementById('hide3').addEventListener('click',function(){
    const pasfild = document.getElementById('inputPL');
    if(pasfild.type === "password"){
        pasfild.type = "text";
    }
    else{
        pasfild.type = "password";
    }   
    
});

const createAccount = document.getElementById('create-account')
const loginModal = document.getElementById('kadrrast_login')
const registerModal = document.getElementById('kadrrastsignup')
createAccount.addEventListener("click", ()=>{
    registerModal.style.display = "block";
    loginModal.style.display = "none";
})

const backtoLogin = document.getElementById('backtoLogin')
backtoLogin.addEventListener("click", ()=>{
    registerModal.style.display = "none";
    loginModal.style.display = "block";
})

const submitAccount = document.getElementById('submit')
const emailModal = document.getElementById('kadrrast_chekemail')
const emailInput = document.getElementById('email1');

function email(){
    return emailInput
}
var emailSent = null

const loginButton = document.getElementById('loginbtn')
loginButton.addEventListener("click",()=>{
    emailModal.style.display = 'none'
    loginModal.style.display = 'block'
})

document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');

    const button = document.getElementById('submit');
    console.log('Button:', button);

    const nameInput = document.getElementById('username');
    const emailInput = document.getElementById('email1');
    const passwordInput = document.getElementById('inputp1');

    button.addEventListener('click', (event) => {
        event.preventDefault();  // Prevent the default button click behavior

        const data = {
            username: nameInput.value,
            email: emailInput.value,
            password: passwordInput.value
        };
        emailModal.style.display = 'block';
        registerModal.style.display = 'none';
        emailSent = emailInput.value
        const emailSent1 = document.getElementById('emailSent')
        emailSent1.innerHTML = emailSent

        console.log('Sending data to server...');

        fetch('/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err });
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            // Handle success response if needed
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');

    const button = document.getElementById('loginbtn2');
    console.log('Button:', button);

    const textInput = document.getElementById('text');
    const passwordInput = document.getElementById('inputPL');

    button.addEventListener('click', (event) => {
        event.preventDefault();  // Prevent the default button click behavior

        const data = {
            text: textInput.value,
            password: passwordInput.value
        };
        // emailModal.style.display = 'block';
        // registerModal.style.display = 'none';
        emailSent = textInput.value
        const emailSent1 = document.getElementById('emailSent')
        emailSent1.innerHTML = emailSent

        console.log('Sending data to server...');

        fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err });
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            // Handle success response if needed
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});