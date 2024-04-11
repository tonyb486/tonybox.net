import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.6.0';

const status = document.getElementById('status');

status.textContent = 'Loading model...';
const model = await pipeline('zero-shot-classification', 'Xenova/mobilebert-uncased-mnli', { function(e) { console.log(e) } } )

status.textContent = 'Ready';

// Buttons
const bname = document.getElementById('bname');
const detect = document.getElementById('detect');
bname.disabled = detect.disabled = false

// Result bar
const resultbar = document.getElementById('resultbar');
const resultthing = document.getElementById('resultthing');

detect.addEventListener("click", async (e) => {
    status.textContent = "Processing...";
    const classification = await model(bname.value, "music band name");
    const score = classification.scores[0]

    if (score > 0.7) status.textContent = "Hey - '"+bname.value+"' might be a band name!";
    else if (score > 0.4) status.textContent = "I dunno if '"+bname.value+"' is a band name...";
    else status.textContent = "Hmm - '"+bname.value+"' might not be a band name.";

    resultbar.style.display = "block"
    resultthing.style.display = "block"
    resultthing.style.marginLeft = Math.floor(score*200-100)+"%"

    resultbar.textContent = Math.floor(score*100)+"% BAND NAME"
})