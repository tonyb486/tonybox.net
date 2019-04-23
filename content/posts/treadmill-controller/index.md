---
title: "Controlling a Treadmill with a Headphone Cable"
date: 2019-04-18
draft: true
tags: ["Programming", "Web Dev"]
description: "Generating tones that control an iFit treadmill on a mobile device using WebAudio."
---

<!-- This article is a draft.  I'm publishing it in my git repository and github in the interest of transparency and so you can observe my thought process if that interests you, but please note that it may have errors, typos, and factual inaccuracies.  I'm still in the process of writing it, and writing the code upon which it relies.  Thanks. -->

<!-- Status: I've ordered an iFit CD on eBay, and I'm waiting for it to arrive.  I have the source code to my older version, based on old forum posts that I can no longer find, but I'd like to go down the rabbit hole once more and observe it from the real thing.  -->

A few years ago, I had a treadmill with an interesting property: it had two 3.5mm headphone jacks.  One of them was an input, and the other was an output.  What made this even more peculiar was that the machine didn't have speakers, and yet it expected you to use a 3.5mm patch cable to route your audio through it.  I set out to figure out why, and eventually ended up with a web app that could control my treadmill using only bursts of audio that turned out to be a modulation of a digital signal.

I no longer have that treadmill, but this was such a cool project with an interesting result, and I regretted that I never found the time to write it up, since others may have similar compatible treadmills.  For this post, I'll be rewriting my older code that generated a WAV file, and replacing it with newer JavaScript that uses WebAudio to generate the tones.  

If you have one of these treadmills and decide to try this out, please let me know by [reaching out to me](/posts/contact).  I haven't been able to test it out on my own, but I know that the older version worked, and I've written this to produce the same audio bursts.  I'm sure these treadmills are still out there, and I hope this post can serve as a reference to those trying to hack their exercise equipment.

<!--
When I made the first version of this project, it was during the all-too-brief period when my pocket smartphone had a 3.5mm jack right on it, so that seemed like the perfect platform to target for this project.  It should still work today, with a dongle or perhaps a Bluetooth to 3.5mm adapter, so I'm giving it another go and learning how to use WebAudio in the process. -->

## What was this headphone jack for?

{{% video webm="vid/demo.webm" mp4="vid/demo.mp4" poster="img/play.jpg" %}}

The treadmill had a feature called iFit, which looks to have been a short-lived experiment in interactive fitness from around 20 years ago.  As far as I can tell, treadmills with this feature are no longer being made, and the name iFit has been recycled and recycled again.  The idea was that they would sell audio CDs with music and narration from fitness instructors, and the audio CDs would also contain these bursts of signal in them that could control the treadmill to make it follow the fitness plan of the audio CD.  You'd plug your CD Walkman or cool shoulder-mounted boom box with a 3.5mm patch cable into the treadmill, plug your headphones into the output of the treadmill, pop in some [sweet tunes](https://www.amazon.com/Treadmill-Level-iFIT-Compatible-Music-Workout/dp/B00J7477RO), and run the night away.  

I went out and purchased a demo CD that looks like new-old-stock, so that I could see what the bursts look like up close, and get a good idea for how they are encoded.  The CD only has one half-hour track for working out to, but it also has some software, and some demo videos.  Above, you can watch a short segment from one of the demo videos, which gives a good idea of what the system was like, back at the turn of the millenium.  In the segment, you can also hear one of the bursts of data, and it should be clear enough to decode even now that it is encoded for the web.  We'll get to that later, though.

## What information is out there about this system?

It's since gotten difficult to find information, because the iFit name was recycled to refer to an SD-card based system, and recycled again to refer to an Internet-based subscription service.  There are programs to generate workouts for those SD cards available online too, such as [this one](https://mwganson.freeyellow.com/workoutgensdonline/) that I stumbled across while looking for information about how this older system worked, but I can't find much more about the older iFit system, apart from some [dead links](https://boards.fool.com/officially-the-ifit-people-say-no-but-someone-18993284.aspx).

I can't find much evidence of the older version  being a colossal success, but I did find some others who have tried to hack it themselves, including a visual basic program  to generate the tones, which made sense in the era.  Indeed, with the audio CD's I've found being dated around 2000-2001, it isn't likely that most people would have a computer that they could just plug into their treadmill, but generating an audio CD with the tones embedded in it would've been nice at the time.

## How does the signal work?

You can hear one of the tones here from the CD's audio track:

{{% audio "aud/sample-tone.mp3" %}}

Did you hear it in the middle?  It sounds like two quick and incredibly short bursts of static.  They're actually bursts of audio that contain a digital signal which is modulated using [amplitude shift keying](https://en.wikipedia.org/wiki/Amplitude-shift_keying).  This is a very simple way to encode data into an audio signal - it works kind of like morse code, except with 0s and 1s representing integers instead of letters, and done much faster.  The carrier wave, in this case a 2000 Hz sine wave, at full amplitude for a period of time represents a 1, and silence for an equal period of time represents a 0. 

To illustrate this, I took the burst, rendered the waveform with Audacity, and annotated it to show the different components of the signal.  You can see the binary data in the bursts match up to the instructor's description of what the treadmill will do when it detects the tone:

{{% image "img/ask.png"  %}}

As shown above, the signal uses a 2000 Hz sine wave as the carrier.  Thus, a 2000 Hz sine tone represents a 1, and silence represents a zero.  The bursts are repeated twice (only one is shown), and contain 30 bits of information that make up the speed, the incline level, and a checksum that is the sum of these two values.  These 8-bit values are transmitted in binary LSB-first (so, backwards), and separated by a 0 and 1 marker, which I suspect may be used for timing.  




## Representing an audio wave digitally with PCM

**TODO: Lolipop Diagram**

## Generating tones with WebAudio

## A simple workout controller






