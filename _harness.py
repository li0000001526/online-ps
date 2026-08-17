# -*- coding: utf-8 -*-
"""在线PS headless 测试装置: 注入测试运行器 -> Chrome headless 执行 -> 解析结果"""
import re, subprocess, sys, os, html as htmlmod

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'index.html')
OUT = os.path.join(BASE, '_headless_test.html')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
UDD = os.path.join(BASE, '_chrome_profile')

ERR_SCRIPT = """<script>
window.__hdrr = [];
window.addEventListener('error', function(e){ window.__hdrr.push('JSERR: '+(e.message||'')+' @'+(e.lineno||0)+':'+(e.colno||0)); });
</script>
"""

RUNNER = """<script>
(function(){
  var L = [];
  var finish = function(){
    var pre = document.createElement('pre');
    pre.id = '__hdrr_out__';
    pre.textContent = L.join('\\n');
    document.body.appendChild(pre);
    document.title = 'HDRR_DONE';
  };
  var runDemo = function(){
    try{
      var A = window.PS.api;
      A.newDoc(960, 600, 'white');
      A.setColor('#e85d5d');
      A.brushStroke(120,140,460,140); A.brushStroke(460,140,460,360); A.brushStroke(460,360,120,360); A.brushStroke(120,360,120,140);
      A.setColor('#ffd35d'); A.brushStroke(150,170,430,170); A.brushStroke(150,195,430,195);
      A.setColor('#5d9de8'); A.fillAt(150,210,30);
      A.setColor('#2b2b2b'); A.addShape('ellipse',520,170,260,200);
      A.setColor('#ffffff'); A.addText(560,220,'Zaixian',46,'#ffffff'); A.addText(560,275,'PS',40,'#ffffff');
      A.setColor('#e85d5d'); A.addShape('arrow',140,460,520,460);
      A.setColor('#5d9de8'); A.addShape('line',140,485,700,485);
      A.setColor('#2b2b2b'); A.addText(160,430,'Made with',22,'#555555');
      A.zoomFit();
    }catch(e){ L.push('DEMO_ERR: '+e.message); }
  };
  try{
    if(!window.PS){ L.push('FATAL: window.PS undefined - app init failed'); finish(); return; }
    var R = window.PS.__selfTest.unit();
    L.push('UNIT ' + R.pass + '/' + R.total);
    R.results.forEach(function(r){ L.push((r.ok?'PASS ':'FAIL ')+r.name); });
    window.PS.__selfTest.flow().then(function(F){
      L.push('FLOW ' + F.pass + '/' + F.total);
      F.results.forEach(function(r){ L.push((r.ok?'PASS ':'FAIL ')+r.name+(r.extra?' ('+r.extra+')':'')); });
      runDemo();
      L.push('DEMO_READY');
      finish();
    }, function(err){ L.push('FLOW_REJECT: '+err.message); runDemo(); finish(); });
  }catch(e){ L.push('FATAL: '+e.message); finish(); }
})();
</script>
"""

def build():
    s = open(SRC, encoding='utf-8').read()
    if '_hdrr_out__' in s:
        print('ERROR: index.html already contains harness markers')
        sys.exit(1)
    s = s.replace('<head>', ERR_SCRIPT + '<head>', 1)
    s = s.replace('</body>', RUNNER + '</body>', 1)
    open(OUT, 'w', encoding='utf-8').write(s)
    print('built', OUT, len(s), 'chars')

def run_dump():
    cmd = [CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
           '--no-default-browser-check', '--user-data-dir=' + UDD,
           '--dump-dom', 'file:///' + OUT.replace('\\', '/').replace(' ', '%20')]
    r = subprocess.run(cmd, capture_output=True, timeout=90, text=True, errors='replace')
    dom = r.stdout
    m = re.search(r'<pre id="__hdrr_out__">(.*?)</pre>', dom, re.S)
    if not m:
        print('NO RESULT NODE. exit=', r.returncode)
        print('STDERR tail:', r.stderr[-800:] if r.stderr else '')
        # 尝试找 title 判断
        t = re.search(r'<title>(.*?)</title>', dom, re.S)
        print('title:', t.group(1) if t else 'N/A')
        return False
    text = htmlmod.unescape(m.group(1))
    print(text)
    return '[FAIL]' not in text and 'FAIL ' not in text and 'FATAL' not in text and 'JSERR' not in text and 'FLOW_REJECT' not in text

def run_shot():
    shot = os.path.join(BASE, '_screenshot.png')
    cmd = [CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
           '--no-default-browser-check', '--user-data-dir=' + UDD,
           '--window-size=1680,1050', '--hide-scrollbars',
           '--screenshot=' + shot, 'file:///' + OUT.replace('\\', '/').replace(' ', '%20')]
    subprocess.run(cmd, capture_output=True, timeout=90)
    if os.path.exists(shot):
        print('screenshot saved:', shot, os.path.getsize(shot), 'bytes')
        return shot
    print('screenshot FAILED')
    return None

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'dump'
    build()
    if mode == 'dump':
        ok = run_dump()
        sys.exit(0 if ok else 2)
    elif mode == 'shot':
        run_shot()
