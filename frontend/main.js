window.addEventListener("DOMContentLoaded", (event) => {
    getVisitCount();
})

const functionAppAzure = "https://getresumecountfunc.azurewebsites.net/api/ResumeCountFunc?";
const functionApiLocal = "http://localhost:7071/api/ResumeCountFunc";

const getVisitCount = () => {
    let count = 1;
    fetch(functionAppAzure).then(response => {
        return response.json()
    }).then(response => {
        console.log("Website called function API.");
        count = response.counter;
        document.getElementById("counter").innerText = count;
    }).catch(function(error){
        console.log(error);
    });
    return count;
}