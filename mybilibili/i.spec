# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['i', 'myIcon/bi.ico', 'main.py', 'BiliVideoDownload.py', 'video.py', 'titlePage.py', 'IPAgent.py', 'QSS.py', 'USER_AGENT.py'],
             pathex=['/Applications/Python 3.8/save/mybilibili'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='i',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='i.app',
             icon=None,
             bundle_identifier=None)
