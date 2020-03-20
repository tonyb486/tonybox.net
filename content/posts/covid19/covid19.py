import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time, datetime
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

country = "US"
filepath = "/srv/www/tmp/"

covidUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
covidData=pd.read_csv(covidUrl)

countryData = covidData.where(covidData["Country/Region"] == country).dropna(how="all")
countryDaily = pd.DataFrame(countryData.sum(axis=0).iloc[4:])
countryDaily.index = pd.to_datetime(countryDaily.index)

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)

ax.plot(countryDaily)
ax.plot(countryDaily, ".")

ax.set_xticks(pd.date_range(countryDaily.index[0], periods=500, freq='W'), minor=False)
ax.set_xticks(pd.date_range(countryDaily.index[0], periods=100, freq='D'), minor=True)
ax.grid(which='major', alpha=0.9)
ax.grid(which='minor', alpha=0.2)

ax.set_xlabel("Date")
ax.set_ylabel("Cases in %s"%(country))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

start = datetime.date.today() - datetime.timedelta(days=45)
end = datetime.date.today() + datetime.timedelta(days=2)
plt.xlim(start, end)

plt.title("Cases of COVID-19 in %s\nGenerated on %s\nData From: https://github.com/CSSEGISandData/COVID-19/"%(country,time.strftime("%Y-%m-%d @ %H:%M %Z")))

fig.patch.set_alpha(0.)

fig.savefig(filepath+"covid19.png", dpi=300)
fig.savefig(filepath+"covid19.svg", dpi=300)

#### CURVE FIT

import datetime
import scipy.optimize
x0,y0 = zip(*enumerate(list(countryDaily[0])))

f = lambda t, a, b: a**(t-b)
(a,b), _ = scipy.optimize.curve_fit(f, x0, y0)

startdate = datetime.date(2020, 1, 22) + datetime.timedelta(days=b)

x = pd.date_range('2020-01-22', datetime.date.today()+ datetime.timedelta(days=4), freq='D')
ax.plot(x, [f(i,a,b) for i,_ in enumerate(x)], ":", label="Exponential Curve Fit (Factor = %.2f, Start = %s)"%(a, startdate.strftime("%Y-%m-%d")))

fig.patch.set_alpha(0.)

start = datetime.date.today() - datetime.timedelta(days=25)
end = datetime.date.today() + datetime.timedelta(days=6)
plt.xlim(start, end)
plt.title("Exponential Curve Fit for COVID-19 Cases in %s\nGenerated on %s\nData From: https://github.com/CSSEGISandData/COVID-19/"%(country, time.strftime("%Y-%m-%d @ %H:%M %Z")))
plt.legend()

fig.savefig(filepath+"covid19-fit.png", dpi=300)
fig.savefig(filepath+"covid19-fit.svg", dpi=300)

## Logistic Fits!

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)

ax.plot(countryDaily, label="Actual Data", linewidth=1)
ax.plot(countryDaily, ".")

ax.set_xticks(pd.date_range(countryDaily.index[0], periods=100, freq='W'), minor=False)
ax.set_xticks(pd.date_range(countryDaily.index[0], periods=100, freq='D'), minor=True)
ax.grid(which='major', alpha=0.9)
ax.grid(which='minor', alpha=0.2)

ax.set_xticks(pd.date_range(countryDaily.index[0], periods=500, freq='W'), minor=False)
ax.set_xticks(pd.date_range(countryDaily.index[0], periods=100, freq='D'), minor=True)
ax.grid(which='major', alpha=0.9)
ax.grid(which='minor', alpha=0.2)

ax.set_xlabel("Date")
ax.set_ylabel("Cases in %s"%(country))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

start = datetime.date.today() - datetime.timedelta(days=30)
end = datetime.date.today() + datetime.timedelta(days=15)
plt.xlim(start, end)

x = pd.date_range('2020-01-22', datetime.date.today()+ datetime.timedelta(days=15), freq='D')

## First Logistic Fit

fig.patch.set_alpha(0.)
b = len(x0)+3
fL = lambda t, L: L/(1 + np.exp((1-a)*(t-b)))
L, _ = scipy.optimize.curve_fit(fL, x0, y0)

startdate = datetime.date(2020, 1, 22) + datetime.timedelta(days=b)
ax.plot(x, [fL(i,L) for i,_ in enumerate(x)], ":", label="Logistic Fit (%.2f, L=%d, Assuming Inflection ~%s)"%(a, L, startdate.strftime("%Y-%m-%d")))

plt.title("Hypothetical Logistic Fit for COVID-19 Cases in %s\nGenerated on %s\nData From: https://github.com/CSSEGISandData/COVID-19/"%(country,time.strftime("%Y-%m-%d @ %H:%M %Z")))
plt.legend()

fig.savefig(filepath+"covid19-logistic-fit.png", dpi=300)
fig.savefig(filepath+"covid19-logistic-fit.svg", dpi=300)

## Second Logistic Fit

b = len(x0)+10
L, _ = scipy.optimize.curve_fit(fL, x0, y0)

startdate = datetime.date(2020, 1, 22) + datetime.timedelta(days=b)
ax.plot(x, [fL(i,L) for i,_ in enumerate(x)], ":", label="Logistic Fit (%.2f, L=%d, Assuming Inflection ~%s)"%(a, L, startdate.strftime("%Y-%m-%d")))
plt.title("Hypothetical Logistic Fit for COVID-19 Cases in %s\nGenerated on %s\nData From: https://github.com/CSSEGISandData/COVID-19/"%(country,time.strftime("%Y-%m-%d @ %H:%M %Z")))
plt.legend()

fig.savefig(filepath+"covid19-logistic-fit2.png", dpi=300)
fig.savefig(filepath+"covid19-logistic-fit2.svg", dpi=300)