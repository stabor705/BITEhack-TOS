Array.from(document.getElementsByClassName("empty-transformation"))
    .forEach((element) => {
        element.addEventListener("click", transformationClicked)
    })

Array.from(document.getElementsByClassName("choice"))
    .forEach((element) => {
        element.addEventListener("click", choiceClicked)
    })

let selected = null;
let lastChoice = null;

function transformationClicked(event) {
    let element = event.currentTarget;
    if (selected != null) {
        toggleSelected(selected)
    }
    selected = element;
    toggleSelected(element);
}

function toggleSelected(element) {
    let className = "transformation";
    if (element.innerHTML.trim() == "")
        className += " empty-transformation";
    if (!element.getAttribute("class").endsWith("selected"))
        className += " selected";
    element.className = className;
}

function choiceClicked(event) {
    if (selected == null)
        return;
    let element = event.currentTarget;
    insertChoice(selected, element);
}

function insertChoice(element, choice) {
    let inIdx = element.getAttribute("data-idx");
    let input = document.getElementById("in-" + inIdx);
    let choiceIdx = choice.getAttribute("data-idx");
    element.setAttribute("class", "transformation");
    if (element.innerHTML.trim() != "") {
        lastChoice.innerHTML = element.innerHTML;
        lastChoice.hidden = false;
    }
    element.innerHTML = choice.innerHTML;
    choice.innerHTML = "";
    choice.hidden = true;
    input.value = choiceIdx;
    console.log(input);
    selected = null;
    lastChoice = choice;
}