//topに戻る処理
document.getElementById('UpButton').addEventListener('click', function() {
	
    var UpButton=this
	UpButton.classList.add('highlight');
    window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
      
	setTimeout(function() {
		UpButton.classList.remove('highlight');
	}, 50);
});

//topボタンのフェードイン、フェードアウト
const UpButton=document.getElementById('UpButton');
window.addEventListener('scroll',function(e){
    const top=window.pageYOffset;
    if(top>1000){
        UpButton.style.opacity=1;
    }else{
        UpButton.style.opacity=0;
    }
});