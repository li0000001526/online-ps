/**
 * 在线PS · 完整流程测试 (flow-test.js)
 * 模拟用户操作流: 新建画布 → 画笔 → 油漆桶 → 图层/形状 → 滤镜 → 撤销重做
 *                 → 文字 → 选区删除 → 旋转 → 导出PNG
 * 用法: 打开 index.html 后, 在浏览器控制台粘贴本文件内容并回车
 */
(async function(){
  if(!window.PS || !window.PS.__selfTest){
    console.error('请先打开 index.html 再运行测试');
    return;
  }
  console.log('⏳ 正在运行完整流程测试…');
  const r = await window.PS.__selfTest.flow();
  console.group('在线PS 完整流程测试 ('+r.pass+'/'+r.total+' 通过)');
  r.results.forEach(x=>console[x.ok?'log':'warn']((x.ok?'[PASS]':'[FAIL]')+' '+x.name+(x.extra?'  ('+x.extra+')':'')));
  console.groupEnd();
  console.log(r.fail===0?'✅ 全部通过':'❌ '+r.fail+' 项失败');
})();
