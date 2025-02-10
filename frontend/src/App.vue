<template>
  <div id="app">
    <div v-if="!user">
      <LoginForm v-if="currentView === 'login'" 
        @login-success="handleLoginSuccess" 
        @switch="switchView" />
      <RegisterForm v-else 
        @register-success="handleRegisterSuccess" 
        @switch="switchView" />
    </div>
    <div v-else>
      <div class="welcome">
        <h2>Welcome, {{ user.username }}!</h2>
        <button @click="logout" class="logout-btn">退出登录</button>
      </div>
      <UserList />
    </div>
  </div>
</template>

<script>
import LoginForm from './components/Login.vue'
import RegisterForm from './components/Register.vue'
import UserList from './components/UserList.vue'

export default {
  name: 'App',
  components: {
    LoginForm,
    RegisterForm,
    UserList
  },
  data() {
    return {
      currentView: 'login',
      user: null
    }
  },
  methods: {
    switchView(view) {
      this.currentView = view
    },
    handleLoginSuccess(userData) {
      this.user = userData
    },
    handleRegisterSuccess() {
      this.currentView = 'login'
      alert('注册成功！请登录')
    },
    logout() {
      this.user = null
      this.currentView = 'login'
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.welcome {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.logout-btn {
  padding: 8px 20px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}
</style>
