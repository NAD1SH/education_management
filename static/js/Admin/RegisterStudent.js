// import { ApiCall, showData } from "./ApiCall";

const Register_Form = document.getElementById('RegisterForm')

// CSRF TOKEN
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
const csrftoken = getCookie('csrftoken');

// ++++++++##############++++++++ \\

// new student register after form submition

Register_Form.addEventListener('submit', event => {
    event.preventDefault()
    let Username = document.getElementsByName('username').value;
    let Password = document.getElementsByName('password').value;
    let Email = document.getElementsByName('eamil').value;
    let Reg_No = document.getElementsByName('reg_no').value;
    let Name = document.getElementsByName('name').value;
    let Batch = document.getElementsByName('batch').value;
    let Department = document.getElementsByName('department').value;

    let API_URL = "http://127.0.0.1:8000/Admin/CreateStudent/";

    let Fetch_Options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            "username" : Username,
            "password" : Password,
            "email" : Email,
            "reg_no" : Reg_No,
            "name" : Name,
            "batch" : Batch,
            "department" : Department,
        })
    };

    fetch(API_URL, Fetch_Options)
        .then(response => {
            // ApiCall()
        });

})
