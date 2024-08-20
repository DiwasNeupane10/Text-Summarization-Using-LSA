function uploadFile() {
    var formData = new FormData();//create a new instance of formdata
    var fileInput = document.getElementById('inputGroupFile02');//select the input with its id
    formData.append('file', fileInput.files[0]);
    /*
    
    'file' is the key sent to the sever
    fileinput.files[0] specifies the first and in this case the only file selected by the user
    
    */

    fetch('/', {
        method: 'POST',
        body: formData
    })
    
    // fetch is an api that sends request to the route /    
    
    .then(response => response.json())
    .then(data => {
        if(data.error)
            alert(data.error);
        else
            alert(data.message);    
       
    })
    .catch((error) => {
        alert('File upload failed!');
    });
}
