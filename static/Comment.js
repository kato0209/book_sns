//textareaのフォームサイズ自動変更
 var form=document.getElementById('CommentForm');
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

//評価機能
const STARS=document.getElementsByClassName('stars');
for(const star of STARS){
    var rating=star.getAttribute('name')
    var starID=star.getAttribute('id')
    var starN=parseInt(starID.slice(-1))
    if(starN<=rating){
        star.classList.add('stars-yellow')
    }
}

