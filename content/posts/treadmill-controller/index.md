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

I no longer have that treadmill, but this was such a cool project with an interesting result, and I regretted that I never found the time to write it up, since others may have similar compatible treadmills.  For this post, I'll be rewriting my older code that generated a WAV file with newer JavaScript that uses WebAudio to generate the tones.  

If you have one of these treadmills and decide to try this out, please let me know by [reaching out to me](/posts/contact).  I haven't been able to test it out on my own, but I know that the older version worked, and I've written this to produce the same audio bursts.  I'm sure these treadmills are still out there, and I hope this post can serve as a reference to those trying to hack their exercise equipment.

## What was the point of this feature?

The treadmill had a feature called iFit, which looks to have been a short-lived experiment in interactive fitness from several years ago.  As far as I can tell, treadmills with this feature are no longer being made.  The idea was that they would sell audio CDs with music and narration from fitness instructors, and the audio CDs would also contain these bursts of signal in them that could control the treadmill to make it follow the fitness plan of the audio CD.  You'd plug your CD Walkman or cool shoulder-mounted boom box with a 3.5mm patch cable into the treadmill, plug your headphones into the output of the treadmill, pop in some [sweet tunes](https://www.amazon.com/Treadmill-Level-iFIT-Compatible-Music-Workout/dp/B00J7477RO), and run the night away.  

It's gotten more confusing since, because the iFit name now refers to an SD-card based system, and there are programs to generate workouts for those SD cards available online too, such as [this one](https://mwganson.freeyellow.com/workoutgensdonline/) I stumbled across while looking for information about how this older system worked.

I can't find much evidence of the older version  being a colossal success, but I did find some others who have tried to hack it themselves, including a visual basic program  to generate the tones, which made sense in the era, although all I can find now are [dead links](https://boards.fool.com/officially-the-ifit-people-say-no-but-someone-18993284.aspx).  Indeed, with the audio CD's I've found being dated around 2001, it isn't likely that most people would have a computer that they could just plug into their treadmill.   

When I made the first version of this project, it was during the all-too-brief period when my pocket smartphone had a 3.5mm jack right on it, so that seemed like the perfect platform to target for this project.  It should still work today, with a dongle or perhaps a Bluetooth to 3.5mm adapter, so I'm giving it another go and learning how to use WebAudio in the process.

## How does the signal work?

The treadmill responds to bursts of audio that contain a digital signal which is modulated using [amplitude shift keying](https://en.wikipedia.org/wiki/Amplitude-shift_keying) on a 2000 Hz sine wave carrier.  Don't be frightened, this is an extremely simple modulation scheme, so simple that we can easily generate PCM samples for it ourselves, and I'll have plenty of diagrams to explain it.  

{{% image "img/ask.svg"  %}}

The modulation scheme here only has two levels: a 2000 Hz sine wave at full amplitude is a 1, and silence is a 0.   You can see what that looks like below, and you can get an idea for this by opening an iFit CD using Audacity.  

## Representing an audio wave digitally with PCM

**TODO: Lolipop Diagram**

## Generating tones with WebAudio

## A simple workout controller






