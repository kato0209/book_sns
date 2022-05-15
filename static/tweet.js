
const STARS=document.getElementsByClassName('star');
for(const star of STARS){
    var rating=star.parentNode.getAttribute('name');
    if(star.getAttribute('name')<=rating){
        star.style.color='yellow';
    }
}