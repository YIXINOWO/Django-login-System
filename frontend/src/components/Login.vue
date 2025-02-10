<template>
  <div class="login-form">
    <h2>登录</h2>
    <div class="form-group">
      <input type="text" v-model="username" placeholder="用户名" />
    </div>
    <div class="form-group">
      <input type="password" v-model="password" placeholder="密码" />
    </div>
    <button @click="handleLogin">登录</button>
    <p class="switch-link" @click="$emit('switch', 'register')">没有账号？去注册</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('/api/login/', {
          username: this.username,
          password: this.password
        })
        if (response.data.status === 'success') {
          this.$emit('login-success', response.data.user)
        } else {
          this.error = response.data.message
        }
      } catch (error) {
        this.error = error.response?.data?.message || '登录失败'
      }
    }
  }
}
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
}
.form-group {
  margin-bottom: 15px;
}
input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.error {
  color: red;
  margin-top: 10px;
}
.switch-link {
  color: #42b983;
  cursor: pointer;
  margin-top: 10px;
}
</style> 