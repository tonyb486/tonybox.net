---
title: "A Chart of COVID-19 Cases in the US"
date: 2020-03-16
tags: ["Programming"]
description: "A US COVID-19 Chart"
---

Just a simple chart, showing the growth of COVID-19, updated regularly from data published on <a href="https://github.com/CSSEGISandData/COVID-19/">github</a> by CSSE at Johns Hopkins University:

<img alt="A chart based on the data from https://github.com/CSSEGISandData/COVID-19/" src="https://tmp.tonyb.xyz/covid19.svg" style="width: 100%">

And with scipy, we can fit an exponential curve to this data.  In this case, I'm only fitting two variables: the day the exponential growth "began," shown as the start date in the legend below, and the rate at which it has been growing since then, also shown in the legend:

<img alt="A chart with an exponential curve fit, based on the data from https://github.com/CSSEGISandData/COVID-19/" src="https://tmp.tonyb.xyz/covid19-fit.svg" style="width: 100%">

If it looks messed up, then maybe the exponential growth is over, or its possible that I've made a mistake, please don't rely on this data to make any big decisions.

These charts should update automatically.
