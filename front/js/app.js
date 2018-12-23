Vue.use(VueResource);
var owm = new Vue({
    el: '#app',
    data: {
        drinks: []
    },
    methods: {
        loadDrinks: function() {
            this.$http.get('http://192.168.1.106:5000/test').then((data) => {
                this.drinks = data.body.blink;
                console.log(this.drinks);
            });
        }
    },
    mounted: function () {
        this.loadDrinks();
    }
});