<template>
  <div class="app">
    <header>
      <h1>问答平台</h1>
    </header>
    <div class="main-content">
      <router-view></router-view>
    </div>
    <footer>
      <p> 2024 编程题解平台 - </p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  font-family: "PingFang SC", "Microsoft YaHei", Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background: linear-gradient(135deg, #1976D2 0%, #64B5F6 100%);
  color: white;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 500;
}

.subtitle {
  margin: 0.5rem 0 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 1600px;
  margin: 1rem auto;
  padding: 0 2rem;
  box-sizing: border-box;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}

footer {
  text-align: center;
  padding: 1rem;
  background: #f1f1f1;
  color: #666;
  font-size: 0.9rem;
  margin-top: auto;
}

/* 全局样式 */
button {
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-1px);
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.error {
  color: #dc3545;
  text-align: center;
  padding: 1rem;
  background: #fff;
  border-radius: 4px;
  margin: 1rem 0;
}

/* 数学公式样式 */
.katex-display {
  margin: 1em 0;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 0.5em 0;
}

/* 代码块样式 */
pre code {
  border-radius: 4px;
  padding: 1em;
  margin: 0.5em 0;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
}

/* 响应式设计 */
@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .main-content {
    margin: 1rem auto;
  }
}
</style>
