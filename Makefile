all:
	hugo --minify
	git commit -a
	git push tonybox master
	rsync -av public/ tonybox.net:/srv/www/tonybox/

draft:
	hugo -D server