"""Minify embedded JS without changing model data or application logic."""
import base64,json,re,subprocess,sys
from pathlib import Path
p=Path(sys.argv[1]); esbuild=sys.argv[2];s=p.read_text()
match=re.search(r'(<script type="importmap">)(.*?)(</script>)',s,re.S)
imports=json.loads(match.group(2))
for name,url in imports['imports'].items():
 prefix='data:text/javascript;base64,'
 assert url.startswith(prefix)
 raw=base64.b64decode(url[len(prefix):])
 result=subprocess.run([esbuild,'--loader=js','--minify','--target=es2020','--legal-comments=inline'],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 imports['imports'][name]=prefix+base64.b64encode(result.stdout).decode()
print('before',len(s.encode()))
s=s[:match.start(2)]+json.dumps(imports,separators=(',',':'))+s[match.end(2):]
p.write_text(s);print('after',p.stat().st_size)
