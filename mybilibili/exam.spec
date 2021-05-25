# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['exam', 'main.py', 'BiliVideoDownload.py', 'video.py', 'titlePage.py', 'USER_AGENT.py', 'IPAgent.py', 'QSS.py'],
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
          name='exam',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='myIcon/bi.ico')
app = BUNDLE(exe,
             name='exam.app',
             icon='myIcon/bi.ico',
             bundle_identifier=None)
