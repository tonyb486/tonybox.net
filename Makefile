# This is just a simple script to deploy
all:
	rm -rf public
	hugo --minify
	git commit -a
	git push origin master
	rsync -av public/ tonybox.net:/srv/www/tonybox/ --delete

draft:
	hugo -D server --bind 0.0.0.0

