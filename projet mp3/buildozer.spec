[app]

title = Seraphin Ultra Player
package.name = seraphinplayer
package.domain = org.seraphin
source.dir = .
source.include_exts = py,png,jpg,kv,mp3

version = 1.0

requirements = python3,kivy==2.3.1,kivymd,pygame,mutagen,numpy

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.sdk = 24
android.ndk = 23b

[buildozer]

log_level = 2
warn_on_root = 1
