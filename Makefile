# This is just a simple script to deploy
all:
	rm -rf public
	hugo --minify
	git commit -a -S
	git push origin master
	git push github master
	rsync -av public/ tonybox.net:/srv/www/tonybox/ --delete

draft:
	hugo -D server --bind 0.0.0.0

