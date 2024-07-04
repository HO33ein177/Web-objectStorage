// handle file upload

// const selectedFile = document.getElementById("fileUploadInput").files[0];
// console.log(selectedFile.name)
const fileInput = document.getElementById('fileUploadInput');
fileInput.addEventListener('click',()=>{
    console.log("Check!!")
})

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileUploadInput');

    fileInput.addEventListener('change', function() {
        const file = fileInput.files[0];

        if (!file) {
            alert("Please select a file first.");
            return;
        }

        console.log("Sending files");
        const formData = new FormData();
        // formData.append('bucket_name', 'vault141');
        // formData.append('file',file)
        formData.append('file_name', file.name);
        formData.append('file_location', file.webkitRelativePath || file.name);
        // formData.append('file_size',file.size)
        console.log(file.size)
        fetch('/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included for Django
            }
        })
        .then(response => {
            console.log('Raw response:', response);
            return response.text();  // Read the response as text
        })
        .then(text => {
            try {
                const data = JSON.parse(text);  // Try to parse the response as JSON
                console.log('Success:', data);
            } catch (error) {
                console.error('Error parsing JSON:', error, 'Response text:', text);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

// Function to get the CSRF token (assuming you're using Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


//drag and drop

let dropbox;

dropbox = document.getElementById("kadr1");
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);
function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}

function dragover(e) {
  e.stopPropagation();
  e.preventDefault();
}
function drop(e) {
  e.stopPropagation();
  e.preventDefault();

  const dt = e.dataTransfer;
  const files = dt.files;

  handleFiles(files);
}
function handleFiles(files){
    for (let i = 0; i < files.length; i++)
    console.log(files.name)
}

let addPeopleModal = document.getElementById('addpeapelbox')
function closeAddPeople(){
    addPeopleModal.style.display = 'none';
}


let hamberMenu = document.getElementById('hamberMenu')
function getNamesInnerHtml() {
    // Select all elements with the class "names"
    const nameElements = document.querySelectorAll('.classNamess');

    // Initialize an empty array to store the innerHTML
    let namesArray = [];

    // Loop through the NodeList and push the innerHTML to the array
    nameElements.forEach(element => {
        namesArray.push(element.innerHTML.trim());
    });

    // Log the array to the console (for demonstration purposes)
    console.log(namesArray);

    return namesArray;
}
getNamesInnerHtml()

let itemName= ""
const menuName = document.getElementById('menuName')
function threeButtonMenu(e){
    // console.log(e.target, e.currentTarget)
    itemName = e.target.previousElementSibling.previousElementSibling.textContent;
    menuName.innerHTML = itemName
    console.log(itemName)
    hamberMenu.style.display = 'block';
}

function removeFile(){
    sendItemNameToServer(itemName)
    hamberMenu.style.display = 'none'
}

function downloadFile(){
    download(itemName)
    hamberMenu.style.display = 'none'
}


const csrftoken = getCookie('csrftoken');
function sendItemNameToServer(item_name) {
    let itemName = String(item_name)
    let dataFile= new FormData()
    dataFile.append('file_name', itemName)

    console.log(typeof itemName)
    const data = {
    file_name: itemName,
};

fetch('/remove/', {
    method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken // Use the CSRF token retrieved earlier
        },
    body: dataFile,
})
.then(response => response.json())
.then(result => {
    console.log(typeof itemName);
    if (result.status === 'success') {
        console.log(result.message);
        // Optionally hide or remove the item from the DOM
        // e.target.closest('.objectItem').style.display = 'none';
    } else {
        console.error(result.message);
    }
})
.catch(error => console.error('Error:', error));
}


function download(item_name) {
    let itemName = String(item_name)
    let dataFile= new FormData()
    dataFile.append('file_name', itemName)

    console.log(typeof itemName)
    const data = {
    file_name: itemName,
};

fetch('/download/', {
    method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken // Use the CSRF token retrieved earlier
        },
    body: dataFile,
})
.then(response => response.json())
.then(result => {
    console.log(typeof itemName);
    if (result.status === 'success') {
        console.log(result.message);
        // Optionally hide or remove the item from the DOM
        // e.target.closest('.objectItem').style.display = 'none';
    } else {
        console.error(result.message);
    }
})
.catch(error => console.error('Error:', error));
}






let item = document.getElementById('item');
let items =document.getElementsByClassName('objectItem')
// console.log(items)
function openMenu(){
        hamberMenu.style.display = 'block';

}

item.addEventListener('contextmenu', rightClick);

function rightClick(event){
    event.preventDefault();
    hamberMenu.style.display = 'block';
}

let closeHamMenu = document.getElementById('menuName')
closeHamMenu.addEventListener('click',()=>{
    hamberMenu.style.display = 'none';
})


let shareButton = document.getElementById('shareButton')
let shareModal = document.getElementById('addpeapelbox')
shareButton.addEventListener('click',()=>{
    shareModal.style.display = 'block';
})