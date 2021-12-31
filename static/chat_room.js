//スクロール位置を最下部に移動する関数
function scrollToBottom(){
    let messageBody = document.getElementById('chat-room-body');
    window.scroll({
    top:messageBody.scrollHeight,
    behavior:"instant"
});
}
scrollToBottom();

//更新ボタン押下時にscrollToBottomの呼び出し
window.addEventListener('unload', function(e){
    scrollToBottom();
});


//textareaのフォームサイズ自動変更
var form=document.getElementById('msg');
 form.style.lineHeight="20px";
 form.style.height="30px";

 form.addEventListener('input',function(e){
     if(e.target.scrollHeight>e.target.offsetHeight){
         e.target.style.height=e.target.scrollHeight+"px";
     }else{
         var height;
         var lineHeight=Number(e.target.style.lineHeight.replace("px",""));
         while(true){
             height=Number(e.target.style.height.replace("px",""));
             if(e.target.scrollHeight>height){
                 e.target.style.height=e.target.scrollHeight+"px"
                 break;
             }
             e.target.style.height=height-lineHeight+"px";
         }
     }
 });