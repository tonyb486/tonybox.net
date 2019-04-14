all:
	rm -rf public
	hugo --minify
	git commit -a
	git push tonybox master
	rsync -avh public/ tonybox.net:/srv/www/tonybox/
	rsync -avh --delete public/posts tonybox.net:/srv/www/tonybox/posts
	rsync -avh --delete public/tags tonybox.net:/srv/www/tonybox/tags

draft:
	hugo -D --bind 0.0.0.0 server
