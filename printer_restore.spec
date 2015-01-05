# -*- mode: python -*-
a = Analysis(['printer_restore.py'],
             pathex=['C:\\purple'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('chalk.ico', 'chalk.ico',  'DATA')]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='printer_restore.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='chalk.ico')
