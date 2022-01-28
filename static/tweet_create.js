const stars =  document.getElementsByClassName('star');
const Input_rating=document.getElementById('id_rating');

 function starMouseover(e) {
    const index = Number(e.target.getAttribute('name'));
    for(let j=0; j < index; j++) {
        stars[j].style.color='yellow';
    }
}

function starMouseout(e) {
    for (let j=0; j < stars.length; j++) {
        stars[j].style.color='gray';
    }
}

for (let i=0; i < stars.length; i++) {
    stars[i].addEventListener('mouseover', starMouseover);
    stars[i].addEventListener('mouseout',starMouseout)

    stars[i].addEventListener('click', function(e){
        for (let j=0; j < stars.length; j++) {
            stars[j].style.color='gray';
        }
        const index = Number(e.target.getAttribute('name'));
        for(let j=0; j<index; j++) {
            stars[j].style.color='yellow';
        }
        Input_rating.value=index

        for(let j=0; j<stars.length; j++) {
            stars[j].removeEventListener('mouseover', starMouseover);
            stars[j].removeEventListener('mouseout', starMouseout);
        }
    });
}
