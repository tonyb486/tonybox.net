---
title: "Some Charts of COVID-19 Cases in the US"
date: 2020-03-19
tags: ["Math", "Charts", "Programming"]
description: "Some US COVID-19 Charts"
summary: "Some charts showing COVID-19 cases in the US, including a general growth chart, an exponential curve fitting, and a couple of hypothetical logistic curve fittings."
draft: true
---

Here's a simple chart, showing the growth of COVID-19, updated regularly from data published on <a href="https://github.com/CSSEGISandData/COVID-19/">github</a> by CSSE at Johns Hopkins University.  If you'd like more detailed information, they have an excellent [information center](https://coronavirus.jhu.edu/).

<img alt="A chart based on the data from https://github.com/CSSEGISandData/COVID-19/" src="https://tmp.tonybox.net/covid19.svg" style="width: 100%" class="invertable">

## Comparison with Italy

I've seen a lot of people comparing the US's growth of COVID-19 to that of Italy, but on a time delay. For a while, both were growing at a very similar rate, and Vox made an [interesting chart](https://www.vox.com/future-perfect/2020/3/20/21179040/coronavirus-us-italy-not-overreacting) comparing the two recently.  I made a similar chart, which updates as the John's Hopkins data updates, shown below:

<img alt="A chart based on the data from https://github.com/CSSEGISandData/COVID-19/ comparing the US and Italy" src="https://tmp.tonybox.net/covid19-us-italy.svg" style="width: 100%" class="invertable">

Comparing the amount of deaths, while more morbid, shows (at least, as of this writing) the US is further behind Italy. 

<img alt="A chart based on the data from https://github.com/CSSEGISandData/COVID-19/ comparing the US and Italy in terms of deaths" src="https://tmp.tonybox.net/covid19-us-italy-deaths.svg" style="width: 100%" class="invertable">

## Exponential Fit

With scipy, we can fit an exponential curve to this data.  In this case, I'm only fitting two variables: the day the exponential growth "began," (*i.e.*, the date when there was at least 1 case expected by the curve, from which growth continued exponentially by the shown factor) shown as the start date in the legend below, and the factor by  which it has been growing since then, also shown in the legend:

<img alt="A chart with an exponential curve fit, based on the data from https://github.com/CSSEGISandData/COVID-19/" src="https://tmp.tonybox.net/covid19-fit.svg" style="width: 100%" class="invertable">

<center><small>

(Fitting the function `y = r**(x - timedelta)`)

</small></center>

If it looks messed up, then maybe the exponential growth is over, or its possible that I've made a mistake. I'm no mathematician, so please don't rely on this data to make any decisions - its just for your information.

## Hypothetical Logistic Fits

Now, let's consider fitting a logistic function instead, because this will end. A logistic function starts out exponential, eventually giving way to a plateau.  We don't know when the plateau will happen, and we don't know when the curve will stop being exponential. I suspect that these are largely dependant on the action we take, and it is unlikely that it will only plateau when it infects the entire population.  

These are not predictions, though, because we have to make an assumption about the inflection point, and I don't have enough data or the ability to make a real assumption about that. Instead, I'll propose a couple of hypothetical inflection points, which illustrate the effect that even a small change in this curve can have.

It's also an issue that the current rate is probably inflated due to the growth of testing, and that makes hypotheticals even more unreliable as predictions.  

With those caveats, we can see below the effect of assuming a hypothetical inflection point about ~3 days away, and using the other variables from our previous exponential fit:

<img alt="A chart with an logistic curve fit, based on the data from https://github.com/CSSEGISandData/COVID-19/" src="https://tmp.tonybox.net/covid19-logistic-fit.svg" style="width: 100%" class="invertable">

And here, we can see the effect of assuming a hypothetical inflection point about ~10 days away, which dramatically increases the expected number of total cases, L:

<img alt="A chart with an logistic curve fit, based on the data from https://github.com/CSSEGISandData/COVID-19/" src="https://tmp.tonybox.net/covid19-logistic-fit2.svg" style="width: 100%" class="invertable">

But I'm just a guy who saw [3Blue1Brown's excellent video](https://www.youtube.com/watch?v=Kas0tIxDvrg) on this topic and thought I could try this at home, so take these charts with a healthy heaping of salt.

These graphs update automatically with the data published on github.  

You can see the code that generates this [here](https://github.com/tonyb486/tonybox.net/blob/master/content/posts/covid19/covid19.py).

