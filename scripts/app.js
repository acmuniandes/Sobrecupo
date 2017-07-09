var app = new Vue
({
    el: '#app',
    data:
    {
        lista: [],
        input: '',
        dbInfo: ''
    },
    methods:
    {
        getTest: function (url) 
        {
            axios.get(url).then(function (response) {
                console.log(response);
            }).catch(function (error) {
                console.log(error.message);
            });
    
        },

        recallDB: function()
        {
            axios.get('/db/recall').then(function (response) 
            {
                this.dbInfo = response
            }).catch (function (error) 
            {
                console.log(error)
            })
        }
    }
})