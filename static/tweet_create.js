const StarRatingApp = Vue.createApp({ 
    data:()=>({
        rating:0
    }),
    methods:{
        selectRating(rating){
            star_rating_ele=document.getElementById('id_rating')
            star_rating_ele.value=this.rating
        },
        setRating(rating){
            this.rating=rating
        }
    }
})
StarRatingApp.component('star-rating', VueStarRating.default)
StarRatingApp.config.compilerOptions.delimiters = ['[[', ']]']
StarRatingApp.mount('#star_rating')