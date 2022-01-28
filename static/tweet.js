const deleteModalButtons = document.getElementsByClassName('del_confirm');
const deleteButton = document.getElementById('del_url');

for (const button of deleteModalButtons) {
    button.addEventListener('click', function() {
    deleteButton.setAttribute("href",button.dataset.deleteurl)
   });
}

const STARS=document.getElementsByClassName('star');
for(const star of STARS){
    var rating=star.parentNode.getAttribute('name');
    if(star.getAttribute('name')<=rating){
        star.style.color='yellow';
    }
}