all:
	hugo --minify
	git commit -a
	git push tonybox master
	rsync -av public/ tonybox.net:/srv/www/tonybox/
	rsync -av public/posts tonybox.net:/srv/www/tonybox/posts --delete
	rsync -av public/tags tonybox.net:/srv/www/tonybox/tags --delete

draft:
	hugo -D server
