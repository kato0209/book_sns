//topに戻る処理
const UpButton=document.getElementById('UpButton');
UpButton.addEventListener('click', function() {
	
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
window.addEventListener('scroll',function(e){
    const top=window.pageYOffset;
    if(top>1000){
        UpButton.style.opacity=1;
    }else{
        UpButton.style.opacity=0;
    }
});