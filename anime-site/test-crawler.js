// 测试最新更新API的脚本
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

async function testLatestUpdateAPI() {
  console.log('测试最新更新API...');
  
  try {
    // 测试GET请求
    console.log('1. 测试GET请求...');
    const getUrl = 'http://localhost:3000/api/latest-update?real=true&limit=5&save=true';
    
    const response = await fetch(getUrl);
    const data = await response.json();
    
    console.log('状态码:', response.status);
    console.log('成功:', data.success);
    console.log('数据条数:', data.total_count);
    
    if (data.filePath) {
      console.log('文件已保存:', data.filePath);
      
      // 验证文件是否存在
      if (fs.existsSync(data.filePath)) {
        console.log('✅ 文件验证成功');
        const fileContent = fs.readFileSync(data.filePath, 'utf8');
        const fileData = JSON.parse(fileContent);
        console.log('文件数据条数:', fileData.total_count);
      } else {
        console.log('❌ 文件未找到');
      }
    }
    
    // 测试POST请求
    console.log('\n2. 测试POST请求...');
    const postUrl = 'http://localhost:3000/api/latest-update';
    
    const postResponse = await fetch(postUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        useRealData: true,
        limit: 3,
        saveToFile: true
      })
    });
    
    const postData = await postResponse.json();
    console.log('POST状态码:', postResponse.status);
    console.log('POST成功:', postData.success);
    console.log('POST数据条数:', postData.total_count);
    
    if (postData.filePath) {
      console.log('POST文件已保存:', postData.filePath);
    }
    
    console.log('\n✅ API测试完成！');
    
  } catch (error) {
    console.error('测试失败:', error.message);
  }
}

// 如果直接运行
if (require.main === module) {
  testLatestUpdateAPI();
}

module.exports = { testLatestUpdateAPI };