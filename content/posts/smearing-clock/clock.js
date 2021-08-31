var febLength, febTime, marTime, correctionFactor, lastCorrectedTime

function initClock() {
    year = new Date().getFullYear()
    febTime = (new Date("02/01/"+year).getTime())
    marTime = (new Date("03/01/"+year).getTime())
    febLength = marTime-febTime
    var realLength = 28*60*60*24*1000
    correctionFactor = realLength/febLength

    explanation = ""
    explanation += "<li>In your time zone, February began at "+Math.floor(febTime/1000)+", unix time.</li>"
    explanation += "<li>In your time zone, February ends at "+Math.floor(marTime/1000)+", unix time.</li>"
    explanation += "<li>February is "+Math.floor(febLength/1000)+" seconds ("+febLength/1000/60/60/24+" days) long this year."+"</li>"
    explanation += "<li>February is "+realLength/1000+" seconds long (28 days) in non-leap-years."+"</li>"

    document.getElementById("main_explanation").innerHTML = explanation

    computeTime();
    setInterval(computeTime, 10)
}
function computeTime() {
    curTime = (new Date()).getTime()
    febSince = curTime-febTime
    correctedTime = new Date(febTime + (febSince*correctionFactor))
    if(Math.floor(correctedTime/1000) == lastCorrectedTime) return;
    lastCorrectedTime = Math.floor(correctedTime/1000)

    if (correctionFactor == 1) {
        document.getElementById("current_explanation").innerHTML = "<li><b>It is not a leap year, so no adjustment is needed.</b></li>"
        document.getElementById("time").innerHTML = "<b>"+(new Date())+"</b>"
    } else if (curTime > marTime || curTime < febTime) {
        document.getElementById("current_explanation").innerHTML = "<li><b>It is not Feburary, so no adjustment is needed.</b></li>"
        document.getElementById("time").innerHTML = "<b>"+(new Date())+"</b>"
    } else {
        explanation = "";
        explanation += "<li><b>We can correct for this by expanding 28 days into "+Math.floor(febLength/1000)+" seconds.</b></li>"
        explanation += "<li>To calculate the corrected time, note that it is now "+Math.floor(curTime/1000)+", unix time.</li>"
        explanation += "<li>Thus, February began "+Math.floor(febSince/1000)+" seconds ago in your time zone."+"</li>"
        explanation += "<li>But, if things were going  ~"+((1-correctionFactor)*100).toFixed(5)+"% slower this would be "+Math.floor((febSince*correctionFactor)/1000)+" seconds ago."+"</li>"
        explanation += "<li>The corrected time is that many seconds since February began, or "+Math.floor(correctedTime.getTime()/1000)+", unix time.</li>"
        explanation += "<li>In real time, this corresponds to "+correctedTime+".</li>"

        document.getElementById("current_explanation").innerHTML = explanation
        document.getElementById("time").innerHTML = "<h3>"+correctedTime+"</h3>"
    }

}

window.onload = initClock