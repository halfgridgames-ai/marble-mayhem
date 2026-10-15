# Builds the installable GitHub Pages version (web/) from the single-file game (index.html).
import re, hashlib, pathlib
root = pathlib.Path(__file__).parent
src = (root / 'index.html').read_text()
src = src.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', '<script src="three.min.js"></script>')
assert 'cdnjs' not in src
head = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#141c3a">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Marbles">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
'''
body_split = src.index('</style>') + len('</style>')
out = head + src[:body_split] + '\n</head>\n<body>\n' + src[body_split:] + '''
<script>if ('serviceWorker' in navigator && !window.Capacitor) addEventListener('load', () => navigator.serviceWorker.register('sw.js'));</script>
</body>
</html>
'''
(root / 'web' / 'index.html').write_text(out)
import shutil
shutil.copy(root / 'vendor' / 'peerjs.min.js', root / 'web' / 'peerjs.min.js')
shutil.copy(root / 'privacy.html', root / 'web' / 'privacy.html')   # privacy policy page for the Play listing   # online play, loaded only when a room is opened
h = hashlib.sha1((out + (root / 'web' / 'manifest.webmanifest').read_text()).encode())
for icon in ('icon-192.png', 'icon-512.png', 'apple-touch-icon.png'):   # new icons must bust the cache too
    h.update((root / 'web' / icon).read_bytes())
ver = h.hexdigest()[:10]
sw = (root / 'sw-template.js').read_text().replace('__VERSION__', ver)
(root / 'web' / 'sw.js').write_text(sw)
print('built web/ version', ver)
