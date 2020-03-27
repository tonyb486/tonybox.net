import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import time, datetime, scipy.optimize
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Configuration
country = "US"
filepath = "/srv/www/tmp/"
facecolor = "#f6f4ef"

# Ingest Data
covidUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
covidData=pd.read_csv(covidUrl)

deathUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
deathData=pd.read_csv(deathUrl)

# Filter and lightly process the data
countryData = covidData.where(covidData["Country/Region"] == country).dropna(how="all")
countryDaily = pd.DataFrame(countryData.sum(axis=0).iloc[4:])
countryDaily.index = pd.to_datetime(countryDaily.index)

# For a nice display
if country == "US": countryName = "the US"
else: countryName = country

# Set up the graph 
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)

ax.set_xticks(pd.date_range(countryDaily.index[0], periods=500, freq='W'), minor=False)
ax.set_xticks(pd.date_range(countryDaily.index[0], periods=100, freq='D'), minor=True)
ax.grid(which='major', alpha=0.9, linestyle=":")
ax.grid(which='minor', alpha=0.2, linestyle=":")

ax.set_xlabel("Date")
ax.set_ylabel("Cases in %s"%(countryName))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

start = datetime.date.today() - datetime.timedelta(days=45)
end = datetime.date.today() + datetime.timedelta(days=2)
plt.xlim(start, end)

plt.title("Cases of COVID-19 in %s"%(countryName))

ax.text(0.015, 0.97, "Data From: https://github.com/CSSEGISandData/COVID-19/\nChart From: https://tonybox.net/posts/covid19/\nGenerated on %s"%(time.strftime("%Y-%m-%d @ %H:%M %Z")),
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(facecolor='white', edgecolor='lightgray', boxstyle='round'))

# Plot the data
ax.plot(countryDaily)
ax.plot(countryDaily, ".")

fig.patch.set_alpha(0.)
ax.set_facecolor(facecolor)
fig.savefig(filepath+"covid19.png", dpi=300, bbox_inches="tight")
fig.savefig(filepath+"covid19.svg", dpi=300, bbox_inches="tight")

###
# Perform an exponential curve fit
###

# Make an x and y for the existing data
x0,y0 = zip(*enumerate(list(countryDaily[0])))

# Define the function we want to fit, and fit with scipy
f = lambda t, a, b: a**(t-b)
(a,b), _ = scipy.optimize.curve_fit(f, x0, y0)

# Compute the date based on the offset
startdate = datetime.date(2020, 1, 22) + datetime.timedelta(days=b)

# Plot the exponential curve, 4 days ahead
x = pd.date_range('2020-01-22', datetime.date.today()+ datetime.timedelta(days=4), freq='D')
ax.plot(x, [f(i,a,b) for i,_ in enumerate(x)], ":", label="Exponential Curve Fit (Factor = %.2f, Start = %s)"%(a, startdate.strftime("%Y-%m-%d")))

# Zoom out a bit
start = datetime.date.today() - datetime.timedelta(days=25)
end = datetime.date.today() + datetime.timedelta(days=6)
plt.xlim(start, end)
plt.title("Exponential Curve Fit for COVID-19 Cases in %s"%(countryName))
ax.legend(loc="upper left", bbox_to_anchor=[0,.85])

fig.patch.set_alpha(0.)
ax.set_facecolor(facecolor)
fig.savefig(filepath+"covid19-fit.png", dpi=300, bbox_inches="tight")
fig.savefig(filepath+"covid19-fit.svg", dpi=300, bbox_inches="tight")

###
## Perform a logistic curve fit
###

# Configure the graph for these new plots

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)

ax.plot(countryDaily, label="Actual Data", linewidth=1)
ax.plot(countryDaily, ".")

ax.set_xticks(pd.date_range(countryDaily.index[0], periods=100, freq='W'), minor=False)
ax.set_xticks(pd.date_range(countryDaily.index[0], periods=100, freq='D'), minor=True)
ax.grid(which='major', alpha=0.9, linestyle=":")
ax.grid(which='minor', alpha=0.2, linestyle=":")

ax.set_xticks(pd.date_range(countryDaily.index[0], periods=500, freq='W'), minor=False)
ax.set_xticks(pd.date_range(countryDaily.index[0], periods=100, freq='D'), minor=True)
ax.grid(which='major', alpha=0.9, linestyle=":")
ax.grid(which='minor', alpha=0.2, linestyle=":")

ax.set_xlabel("Date")
ax.set_ylabel("Cases in %s"%(countryName))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

start = datetime.date.today() - datetime.timedelta(days=30)
end = datetime.date.today() + datetime.timedelta(days=15)
plt.xlim(start, end)

ax.text(0.015, 0.97, "Data From: https://github.com/CSSEGISandData/COVID-19/\nChart From: https://tonybox.net/posts/covid19/\nGenerated on %s"%(time.strftime("%Y-%m-%d @ %H:%M %Z")),
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(facecolor='white', edgecolor='lightgray', boxstyle='round'))


# We want to predict out 15 days ahead for both
x = pd.date_range('2020-01-22', datetime.date.today()+ datetime.timedelta(days=15), freq='D')

## First Logistic Fit

fig.patch.set_alpha(0.)
b = len(x0)+3
fL = lambda t, L: L/(1 + np.exp((1-a)*(t-b)))
L, _ = scipy.optimize.curve_fit(fL, x0, y0)

startdate = datetime.date(2020, 1, 22) + datetime.timedelta(days=b)
ax.plot(x, [fL(i,L) for i,_ in enumerate(x)], ":", label="Logistic Fit (%.2f, L=%d, Assuming Inflection ~%s)"%(a, L, startdate.strftime("%Y-%m-%d")))

plt.title("Hypothetical Logistic Fit for COVID-19 Cases in %s"%(countryName))
ax.legend(loc="upper left", bbox_to_anchor=[0,.85])

## Add some annotation
a1 = ax.annotate("Hypothetical Inflection Point\n(if things QUICKLY start slowing down)",
            xy=(startdate,fL(b,L)), xytext=(startdate-datetime.timedelta(days=25),fL(b,L)*.8),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3"), ha='left', va='bottom')

ax.set_facecolor(facecolor)
fig.savefig(filepath+"covid19-logistic-fit.png", dpi=300, bbox_inches="tight")
fig.savefig(filepath+"covid19-logistic-fit.svg", dpi=300, bbox_inches="tight")

## Second Logistic Fit

b = len(x0)+10
L, _ = scipy.optimize.curve_fit(fL, x0, y0)

startdate = datetime.date(2020, 1, 22) + datetime.timedelta(days=b)
ax.plot(x, [fL(i,L) for i,_ in enumerate(x)], ":", label="Logistic Fit (%.2f, L=%d, Assuming Inflection ~%s)"%(a, L, startdate.strftime("%Y-%m-%d")))
plt.title("Hypothetical Logistic Fit for COVID-19 Cases in %s"%(countryName))

## Add some annotation
a1.remove() # remove old one
ax.annotate("Hypothetical Inflection Point\n(if things LESS QUICKLY start slowing down)",
            xy=(startdate,fL(b,L)), xytext=(startdate-datetime.timedelta(days=25),fL(b,L)*.8),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3"), ha='left', va='bottom')
ax.legend(loc="upper left", bbox_to_anchor=[0,.85])

ax.set_facecolor(facecolor)
fig.savefig(filepath+"covid19-logistic-fit2.png", dpi=300, bbox_inches="tight")
fig.savefig(filepath+"covid19-logistic-fit2.svg", dpi=300, bbox_inches="tight")


###
# US vs Italy
###

def comparisonChart(dataSource, metric, caseCutoff, countryComparison, filename):
    # Filter and lightly process the data for the US and Italy
    usData = dataSource.where(dataSource["Country/Region"] == "US").dropna(how="all")
    usDaily = pd.DataFrame(usData.sum(axis=0).iloc[4:])
    usDaily.index = pd.to_datetime(usDaily.index)

    cpData = dataSource.where(dataSource["Country/Region"] == countryComparison).dropna(how="all")
    cpDaily = pd.DataFrame(cpData.sum(axis=0).iloc[4:])
    cpDaily.index = pd.to_datetime(cpDaily.index)

    # Find the series starting from >100 cases...
    usRecent = usDaily[(usDaily[0]>=caseCutoff).idxmax():]
    cpRecent = cpDaily[(cpDaily[0]>=caseCutoff).idxmax():]

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)

    # Plot the existing data
    ax.bar(range(0, len(cpRecent)), cpRecent[0], alpha=0.5, label="%s (Starting from %s)"%(countryComparison, cpRecent.index[0].strftime("%Y-%m-%d")), color="C0")
    ax.bar(range(0, len(usRecent)), usRecent[0], alpha=0.5, label="US (Starting from %s)"%(usRecent.index[0].strftime("%Y-%m-%d")), color="C1")

    # Set up the graph
    ax.minorticks_on()
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.grid(which='major', alpha=1.0, linestyle=":", axis="y")
    ax.grid(which='minor', alpha=0.5, linestyle=":", axis="y")
    ax.set_xlim(-1,len(cpRecent),int(np.floor(len(cpRecent)/10)))

    ax.set_title("COVID-19 %ss in the US vs %s"%(metric.capitalize(), countryComparison))
    ax.set_xlabel("Days since %dth %s"%(caseCutoff, metric))
    ax.set_ylabel("Number of %ss"%(metric))


    ## Annotations for clarity
    ax.annotate("Day of %dth %s\n%s for the US\n%s for %s"%(caseCutoff, metric, usRecent.index[0].strftime("%b %d"), cpRecent.index[0].strftime("%b %d"), countryComparison),
                xy=(0, max(ax.get_ylim())/100), xytext=(-.5,max(ax.get_ylim())/10),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    def format_xaxis(x, p=None):
        if x<0: return ""
        x = int(x)
        dayString = "Day %d\n\n"%(x)
        usString = usRecent.index[x].strftime("US: %b %d\n") if x < len(usRecent) else ""
        cpString = cpRecent.index[x].strftime(countryComparison+": %b %d\n") if x < len(cpRecent) else ""
        return dayString+usString+cpString
        
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xaxis))
    ax.locator_params(axis="x", integer=True, nbins=10, prune="both")

    ax.legend(loc="upper left", bbox_to_anchor=[0,.88])
    ax.text(0.015, 0.97, "Data From: https://github.com/CSSEGISandData/COVID-19/\nChart From: https://tonybox.net/posts/covid19/\nGenerated on %s"%(time.strftime("%Y-%m-%d @ %H:%M %Z")),
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(facecolor='white', edgecolor='lightgray', boxstyle='round'))

    ax.annotate("Latest Data\nin the US",
                xy=(len(usRecent)-1, usRecent[0][-1]), xytext=(len(usRecent)-1,usRecent[0][-1]+max(ax.get_ylim())/10),
                arrowprops=dict(arrowstyle="->"), ha='center')

    # Color and Save
    fig.patch.set_alpha(0.)
    ax.set_facecolor(facecolor)
    fig.subplots_adjust(bottom=0.2)
    fig.savefig(filepath+filename+".png", dpi=300, bbox_inches="tight")
    fig.savefig(filepath+filename+".svg", dpi=300, bbox_inches="tight")

# Do the comparison, given the cutoff & country to compare to
comparisonChart(covidData, "case", 100, "Italy", "covid19-us-italy")

# Do the more morbid comparison...
comparisonChart(deathData, "death", 100, "Italy", "covid19-us-italy-deaths")
