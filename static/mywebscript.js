function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseElement = document.getElementById("system_response");

    if (!textToAnalyze.trim()) {
        responseElement.innerHTML = "Invalid text! Please try again!";
        return;
    }

    const xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            responseElement.innerHTML =
                this.status === 200
                    ? this.responseText
                    : "Invalid text! Please try again!";
        }
    };

    xhttp.open(
        "GET",
        "/emotionDetector?textToAnalyze=" +
            encodeURIComponent(textToAnalyze),
        true
    );
    xhttp.send();
}
