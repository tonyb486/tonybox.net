---
title: "Doctor Who-Style Wi-Fi With Sentient Captive Portal"
date: 2013-03-31T12:03:00-04:00
draft: false
tags: ["Mostly Harmless", "Security", "Linux"]
description: "Using a captive portal on a fake WiFi network using hostapd to simulate the effect of stealing the user's soal, as in Doctor Who's The Bells of Saint John."
---

In this week’s episode of Doctor Who, [The Bells of Saint John](https://en.wikipedia.org/wiki/The_Bells_of_Saint_John), the enemy is sentient and living inside of the wifi - specifically, a wifi network with a name consisting of weird symbols would appear, the target would click on it, and it would infest their computer and eventually consume their soul and consciousness into the cloud.
 <!--more-->

{{% video webm="vid/soultheif.webm" mp4="vid/soultheif.mp4" %}}

## How Does It Work?

As you can see in the video above, theres a pretty cool way to make this happen, using a Linux machine with a USB wifi card, hostapd, and a simple web server. 

The reason it opens up by itself on macOS is because macOS tries to automatically detect if there is a captive portal login screen, like those commonly used by coffee shops and such.  In the case of macOS, it does this by sending a request to captive.apple.com; other operating systems also have this feature, and use different servers. 

If the OS can't get the message from its test page, it will open up a web page to allow the user to log in, since it assumes that if it can't get through, it is being redirected to a login page. For this, we’re taking advantage of that by instead loading a web page which will upload the user’s soul.

## Configuration: Wireless Network 
Starting with the ssid, there is a helpful [reddit thread](http://www.reddit.com/r/doctorwho/comments/1bbt6p/i_wonder_if_anyone_will_connect_to_my_guest_wifi) where they provide a few good unicode representations of the symbols shown in the episode, I settled on using “┓┏ 凵 =╱⊿┌┬┐” for my setup.

I hooked up a usb wifi card to my fileserver , which runs debian, and installed hostapd, dnsmasq, and nginx. (this will, of course, work well on a laptop!):

{{<highlight bash>}}
apt-get install hostapd dnsmasq nginx
{{</highlight>}}

Next, I modified the configuration file for hostapd, /etc/hostapd/hostapd.conf, (replacing wlan0 withe the id of your wireless card):

{{<highlight bash>}}
interface=wlan0
ssid=┓┏ 凵 =╱⊿┌┬┐
channel=7
driver=nl80211
hw_mode=g
logger_stdout=-1
logger_stdout_level=2
max_num_sta=10
wpa=0
{{</highlight>}}

Next, I configured debian to use it, by editing a line in /etc/default/hostapd.

{{<highlight bash>}}
DAEMON_CONF="/etc/hostapd/hostapd.conf"
{{</highlight>}}

Next, dnsmasq needs to be configured, I edited the config file to give out DHCP leases, and to return the “router’s” ip for every DNS request, by editing various lines in /etc/dnsmasq/dnsmasq.conf:

{{<highlight bash>}}
# ...
interface=wlan1
# ...
dhcp-range=10.1.0.50,10.1.0.200,12h
# ...
address=/#/10.1.0.1
# ...
{{</highlight>}}

## Configuration: Routing Traffic

To route the HTTP traffic meant for the captive portal test page, forwarded all traffic to the internal server in the style of the classic [upside down ternet](http://www.ex-parrot.com/pete/upside-down-ternet.html):

{{<highlight bash>}}
iptables -t nat -A PREROUTING -s 10.1.0.1/24 -p tcp -j DNAT --to-destination 10.1.0.1
{{</highlight>}}

Finally, I set up nginx to serve out pages normally, the default folder for debian is /usr/share/nginx/www, so this is a fine place to start - I put a video file clipped from the episode, upload.mp4 in that folder, and created a simple index.html:

{{<highlight html>}}
<body style="margin: 0px; background: black">
<video style="width: 100%; height: 100%" autoplay loop>
<source src="upload.mp4" type="video/mp4">
</video>
</body>
{{</highlight>}}

With it all configured, I can start everything up:

{{<highlight bash>}}
/etc/init.d/hostapd start
ifconfig wlan0 10.1.0.1
/etc/init.d/nginx start
/etc/init.d/dnsmasq start
{{</highlight>}}

And the end result is shown in the video above!

<small>
    <b>Updated: March 2019</b> (minor content edits, updated for new blog system)
</small>
