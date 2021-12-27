document.getElementById('id_ProfileImage').addEventListener('change', function (e) {
    
    var file = e.target.files[0];

    var fileReader = new FileReader();
    fileReader.onload = function() {
        
        var dataUri = this.result;

        var img = document.getElementById('preview');
        img.src = dataUri;
    }
    
    fileReader.readAsDataURL(file);
});