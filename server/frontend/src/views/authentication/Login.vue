<template>
<body class="text-center">
  <form class="form-signin" method="post">
    <img class="mb-4" src="" alt height="125" />
    <hr>
    {{message}}
    <!-- <p>Your username and password didn't match. Please try again.</p> -->

    <b-form-input v-model="username" type="text" class="form-control" placeholder="Username" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"/>
    <b-form-input v-model="password" type="password" class="form-control" placeholder="Password" autocomplete="current-password" v-on:keyup.enter="login" />

    <b-button class="btn btn-lg btn-block" style="border: 1px solid gray; color: white;" @click="login">Sign in</b-button>
  </form>
</body>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      message: ""
    };
  },
  methods: {
    login() {
      let self = this
      this.$apollo.mutate({
        mutation: gql`
          mutation($username: String!, $password: String!) {
            login(username: $username, password: $password) {
              isAuthenticated
            }
          }
        `,
        variables: {
          username: self.username,
          password: self.password
        }
      }).then( (data) => {
        self.$router.push({ name: "Dashboard" });
      }).catch( (error) => {
        // console.log(error)
        self.message = "Login error"
      })
    }
  }
};
</script>

<style scoped>
html,
body {
  height: 100%;
}

body {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
}

a {
  color: #cc0000;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
input {
  margin: 2.5px 0 2.5px 0;
}
input:focus input:active {
  outline: none;
}
</style>