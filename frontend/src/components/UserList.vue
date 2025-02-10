<template>
  <div class="user-list">
    <h2>用户列表</h2>
    <table>
      <thead>
        <tr>
          <th>用户名</th>
          <th>邮箱</th>
          <th>年龄</th>
          <th>创建时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.age }}</td>
          <td>{{ user.created_at }}</td>
          <td>
            <button @click="editUser(user)" class="edit-btn">编辑</button>
            <button @click="deleteUser(user.id)" class="delete-btn">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 分页控件 -->
    <div class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
        class="page-btn"
      >
        上一页
      </button>
      <span class="page-info">
        第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
      </span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="changePage(currentPage + 1)"
        class="page-btn"
      >
        下一页
      </button>
    </div>

    <!-- 编辑用户对话框 -->
    <div v-if="showEditDialog" class="edit-dialog">
      <div class="dialog-content">
        <h3>编辑用户</h3>
        <div class="form-group">
          <input type="text" v-model="editingUser.username" placeholder="用户名" />
        </div>
        <div class="form-group">
          <input type="password" v-model="editingUser.password" placeholder="密码（留空则不修改）" />
        </div>
        <div class="form-group">
          <input type="email" v-model="editingUser.email" placeholder="邮箱" />
        </div>
        <div class="form-group">
          <input type="number" v-model="editingUser.age" placeholder="年龄" />
        </div>
        <div class="dialog-buttons">
          <button @click="updateUser" class="save-btn">保存</button>
          <button @click="showEditDialog = false" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserList',
  data() {
    return {
      users: [],
      showEditDialog: false,
      editingUser: null,
      error: '',
      currentPage: 1,
      totalPages: 1
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get(`/api/users/?page=${this.currentPage}`)
        if (response.data.status === 'success') {
          this.users = response.data.users
          this.totalPages = response.data.total_pages
        }
      } catch (error) {
        console.error('获取用户列表失败:', error)
      }
    },
    changePage(page) {
      this.currentPage = page
      this.fetchUsers()
    },
    editUser(user) {
      this.editingUser = { ...user }
      this.editingUser.password = '' // 清空密码字段
      this.showEditDialog = true
    },
    async updateUser() {
      try {
        const response = await axios.put(`/api/users/${this.editingUser.id}/`, this.editingUser)
        if (response.data.status === 'success') {
          this.showEditDialog = false
          this.fetchUsers()
          alert('更新成功')
        } else {
          alert(response.data.message)
        }
      } catch (error) {
        alert(error.response?.data?.message || '更新失败')
      }
    },
    async deleteUser(userId) {
      if (confirm('确定要删除这个用户吗？')) {
        try {
          const response = await axios.delete(`/api/users/${userId}/delete/`)
          if (response.data.status === 'success') {
            this.fetchUsers()
            alert('删除成功')
          }
        } catch (error) {
          alert(error.response?.data?.message || '删除失败')
        }
      }
    }
  }
}
</script>

<style scoped>
.user-list {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
}

.edit-btn, .delete-btn {
  margin: 0 5px;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn {
  background-color: #42b983;
  color: white;
}

.delete-btn {
  background-color: #ff4444;
  color: white;
}

.edit-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
}

.dialog-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.save-btn, .cancel-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn {
  background-color: #42b983;
  color: white;
}

.cancel-btn {
  background-color: #666;
  color: white;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.page-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
}

.page-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #666;
}
</style> 