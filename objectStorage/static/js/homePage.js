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
        formData.append('bucket_name', 'fkljadsgfkfjsdfkl');
        formData.append('file_name', file.name);
        formData.append('file_location', file.webkitRelativePath || file.name);
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