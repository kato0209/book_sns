const STARS=document.getElementsByClassName('stars');
for(const star of STARS){
    var rating=star.getAttribute('name')
    var starID=star.getAttribute('id')
    var starN=parseInt(starID.slice(-1))
    if(starN<=rating){
        star.classList.add('stars-yellow')
    }
}