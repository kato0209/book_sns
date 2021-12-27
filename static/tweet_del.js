const deleteModalButtons = document.getElementsByClassName('del_confirm');
const deleteButton = document.getElementById('del_url');


for (const button of deleteModalButtons) {
   button.addEventListener('click', function() {
       deleteButton.setAttribute("href",button.dataset.deleteurl)
   });
}