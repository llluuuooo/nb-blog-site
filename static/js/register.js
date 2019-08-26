new Vue({
  el: '#register',
  data: {
    username: null,
    password: null,
    repassword: null,
    email: null,
    code: null,
  },
  methods: {
    sentEmail: function() {
      console.log("sent email to:" + this.email);
    },
    onClick: function() {
      if (this.password == this.repassword) {
        console.log("username:" + this.username);
        console.log("password:" + this.password);
        console.log("repassword:" + this.repassword);
        console.log("email:" + this.email);
        console.log("code:" + this.code);
      }
    },
    testPassword: function() {
      var reg = /^\w{6,20}$/;
      return !reg.test(this.password);
    },
    testUsername: function() {
      var reg = /^[\u4E00-\u9FA5A-Za-z0-9]{2,20}$/;
      return !reg.test(this.username);
    },
    testEmail: function() {
      var reg = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
      return !reg.test(this.email);
    },
  },
});
