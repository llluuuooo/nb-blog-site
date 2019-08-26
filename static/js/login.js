new Vue({
  el: '#login',
  data: {
    username: null,
    password: null,
  },
  methods: {
    onClick: function() {
      console.log("username:" + this.username);
      console.log("password:" + this.password);
    },
  }
});
