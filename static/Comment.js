const textarea=document.getElementById('comment_input'); 
textarea.style.lineHeight="20px"; 
textarea.style.height="30px"; 

let clientHeight=textarea.clientHeight
textarea.addEventListener('input', function(){
    textarea.style.height = clientHeight + 'px';
    let scrollHeight = textarea.scrollHeight;
    textarea.style.height = scrollHeight + 'px';
});