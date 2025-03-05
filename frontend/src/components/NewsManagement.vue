<template>
  <div class="news-container">
    <!-- 新闻详情弹窗 -->
    <el-dialog v-model="detailVisible" title="新闻详情" width="700px" class="detail-dialog">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="标题">{{ currentNews.title }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ currentNews.category_name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(currentNews.status)" size="small">
            {{ statusText(currentNews.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="发布时间">{{ currentNews.publish_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="内容">
          <div class="news-content">{{ currentNews.content }}</div>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新建新闻弹窗 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="form.id ? '编辑新闻' : '新建新闻'" 
      width="600px" 
      class="news-dialog"
    >
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" placeholder="请输入标题" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="内容">
          <el-input 
            v-model="form.content" 
            type="textarea" 
            :rows="6" 
            placeholder="请输入新闻内容"
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category_id" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="item in categories"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">提交</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 顶部操作栏 -->
    <div class="top-bar">
      <h2 class="page-title">新闻管理</h2>
      <el-button type="primary" @click="showCreateDialog" icon="Plus">新建新闻</el-button>
    </div>

    <!-- 新闻列表 -->
    <el-card class="news-table-card">
      <el-table 
        :data="newsList" 
        style="width: 100%"
        :header-cell-style="{ background: '#f5f7fa' }"
        border
      >
        <el-table-column prop="title" label="标题" min-width="200">
          <template #default="{ row }">
            <div class="news-title-cell">
              <el-tooltip :content="row.title" placement="top" :show-after="1000">
                <span class="news-title">{{ row.title }}</span>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="category_name" label="分类" width="120" align="center" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">
              {{ statusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publish_time" label="发布时间" width="180" align="center">
          <template #default="{ row }">
            {{ row.publish_time || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" fixed="right" align="center">
          <template #default="{ row }">
            <el-button-group>
              <el-button 
                size="small" 
                type="info"
                @click="showDetail(row)"
                :icon="View"
              >
                详情
              </el-button>
              <el-button 
                size="small" 
                type="primary" 
                @click="editNews(row)"
                :icon="Edit"
              >
                编辑
              </el-button>
              <el-button 
                size="small" 
                :type="row.status === 'published' ? 'warning' : 'success'"
                @click="toggleStatus(row)"
              >
                {{ row.status === 'published' ? '归档' : '发布' }}
              </el-button>
              <el-popconfirm
                title="确定要删除这条新闻吗？"
                @confirm="deleteNews(row.id)"
                confirm-button-text="确定"
                cancel-button-text="取消"
              >
                <template #reference>
                  <el-button 
                    size="small" 
                    type="danger"
                    :icon="Delete"
                  >
                    删除
                  </el-button>
                </template>
              </el-popconfirm>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { Edit, Delete, View } from '@element-plus/icons-vue'

export default {
  data() {
    return {
      dialogVisible: false,
      form: {
        id: null,
        title: '',
        content: '',
        category_id: null
      },
      categories: [],
      newsList: [],
      currentNews: {},
      detailVisible: false,
    }
  },
  mounted() {
    this.fetchNews();
    this.fetchCategories();
  },
  methods: {
    async fetchNews() {
      try {
        const { data } = await this.$axios.get('/news');
        this.newsList = data;
      } catch (error) {
        this.$message.error('获取新闻列表失败');
      }
    },
    statusTagType(status) {
      const types = {
        draft: 'info',
        published: 'success',
        archived: 'warning'
      };
      return types[status] || '';
    },
    async fetchCategories() {
      try {
        const { data } = await this.$axios.get('/categories');
        this.categories = data;
      } catch (error) {
        this.$message.error('获取分类失败');
      }
    },
    showCreateDialog() {
      this.form = {
        id: null,
        title: '',
        content: '',
        category_id: null
      };
      this.dialogVisible = true;
      this.fetchCategories();
    },
    async submitForm() {
      if (!this.form.title.trim()) {
        this.$message.error('标题不能为空');
        return;
      }
      if (!this.form.category_id) {
        this.$message.error('请选择分类');
        return;
      }

      try {
        const formData = {
          title: this.form.title.trim(),
          content: this.form.content.trim(),
          category_id: Number(this.form.category_id),
          status: 'draft'
        };

        if (this.form.id) {
          // 编辑现有新闻
          await this.$axios.put(`/news/${this.form.id}`, formData);
          this.$message.success('更新成功');
        } else {
          // 创建新新闻
          await this.$axios.post('/news', formData);
          this.$message.success('创建成功');
        }

        this.dialogVisible = false;
        this.form = {
          id: null,
          title: '',
          content: '',
          category_id: null
        };
        this.fetchNews();
      } catch (error) {
        console.error('操作失败:', error.response?.data || error);
        this.$message.error(error.response?.data?.message || '操作失败，请检查数据格式是否正确');
      }
    },
    editNews(news) {
      this.form = {
        id: news.id,
        title: news.title,
        content: news.content,
        category_id: news.category_id
      };
      this.dialogVisible = true;
    },
    async deleteNews(id) {
      try {
        await this.$axios.delete(`/news/${id}`);
        this.$message.success('删除成功');
        this.fetchNews();
      } catch (error) {
        this.$message.error('删除失败');
      }
    },
    async toggleStatus(news) {
      try {
        const newStatus = news.status === 'published' ? 'archived' : 'published';
        await this.$axios.patch(`/news/${news.id}/status`, { status: newStatus });
        this.$message.success('状态更新成功');
        this.fetchNews();
      } catch (error) {
        this.$message.error('状态更新失败');
      }
    },
    statusText(status) {
      const texts = {
        draft: '草稿',
        published: '已发布',
        archived: '已归档'
      };
      return texts[status] || status;
    },
    showDetail(news) {
      this.currentNews = { ...news };
      this.detailVisible = true;
    },
  }
}
</script>

<style scoped>
.news-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  margin: 1000;
  color:rgb(46, 103, 218);
  font-size: 24px;
  position: absolute;
 
  left: 50%;
}

.news-table-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.news-title-cell {
  max-width: 500px;
}

.news-title {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.news-dialog :deep(.el-dialog__body) {
  padding: 20px 30px;
}

:deep(.el-button-group) {
  display: flex;
  gap: 8px;
}

:deep(.el-table) {
  --el-table-border-color: #ebeef5;
  --el-table-header-bg-color: #f5f7fa;
}

:deep(.el-table th) {
  font-weight: 600;
}

:deep(.el-tag) {
  min-width: 60px;
}

.detail-dialog :deep(.el-descriptions__body) {
  padding: 20px;
}

.news-content {
  white-space: pre-wrap;
  line-height: 1.6;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

:deep(.el-table__row) {
  td {
    padding: 12px 0;
  }
}

:deep(.el-tag) {
  font-weight: 500;
  padding: 0 8px;
}

:deep(.el-descriptions__label) {
  width: 100px;
  text-align: right;
  color: #606266;
}

:deep(.el-descriptions__content) {
  padding-left: 20px;
}
</style>