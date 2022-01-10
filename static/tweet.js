//プレビュー画像の表示
document.getElementById('id_snsImage').addEventListener('change', function (e) {
    
    var file = e.target.files[0];

    var fileReader = new FileReader();
    fileReader.onload = function() {
        
        var dataUri = this.result;

        var img = document.getElementById('file-preview');
        img.src = dataUri;
    }
    
    fileReader.readAsDataURL(file);
});
console.log(10)
window.onload=function(){
    console.log(1)
    var Imagefile=document.getElementById('id_snsImage').value;
    var fileReader = new FileReader();
    fileReader.onload = function() {
        
        var dataUri = this.result;

        var img = document.getElementById('file-preview');
        img.src = dataUri;
    }
    fileReader.readAsDataURL(Imagefile)
}

