<template>
  <div class="register-form">
    <h2>注册</h2>
    <div class="form-group">
      <input type="text" v-model="username" placeholder="用户名" />
    </div>
    <div class="form-group">
      <input type="password" v-model="password" placeholder="密码" />
    </div>
    <div class="form-group">
      <input type="email" v-model="email" placeholder="邮箱" />
    </div>
    <div class="form-group">
      <input type="number" v-model="age" placeholder="年龄" />
    </div>
    <button @click="handleRegister">注册</button>
    <p class="switch-link" @click="$emit('switch', 'login')">已有账号？去登录</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterForm',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      age: '',
      error: ''
    }
  },
  methods: {
    async handleRegister() {
      try {
        const response = await axios.post('/api/register/', {
          username: this.username,
          password: this.password,
          email: this.email,
          age: parseInt(this.age)
        })
        if (response.data.status === 'success') {
          this.$emit('register-success')
        } else {
          this.error = response.data.message
        }
      } catch (error) {
        this.error = error.response?.data?.message || '注册失败'
      }
    }
  }
}
</script>

<style scoped>
.register-form {
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