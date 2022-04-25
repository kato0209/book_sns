const TweetListApp=Vue.createApp({
    data:()=>({
        delete_url:'#'
    }),
    methods:{
        DeleteButton:function(event){
            this.delete_url=event.target.dataset.deleteurl
        }
    }
})
TweetListApp.config.compilerOptions.delimiters = ['[[', ']]']
TweetListApp.mount('#tweet-list')


const STARS=document.getElementsByClassName('star');
for(const star of STARS){
    var rating=star.parentNode.getAttribute('name');
    if(star.getAttribute('name')<=rating){
        star.style.color='yellow';
    }
}