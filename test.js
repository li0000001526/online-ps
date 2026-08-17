/**
 * 在线PS · 单元测试 (test.js)
 * 用法: 打开 index.html 后, 在浏览器控制台粘贴本文件内容并回车,
 *       或直接在控制台执行 window.PS.__selfTest.unit()
 * 输出: PASS/FAIL 汇总表格
 */
(function(){
  if(!window.PS || !window.PS.__selfTest){
    console.error('请先打开 index.html 再运行测试');
    return;
  }
  const r = window.PS.__selfTest.unit();
  console.group('在线PS 单元测试 ('+r.pass+'/'+r.total+' 通过)');
  r.results.forEach(x=>console[x.ok?'log':'warn']((x.ok?'[PASS]':'[FAIL]')+' '+x.name));
  console.groupEnd();
  console.log(r.fail===0?'✅ 全部通过':'❌ '+r.fail+' 项失败');
})();
