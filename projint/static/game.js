Array.from(document.getElementsByClassName("empty-transformation"))
    .forEach((element) => {
        element.addEventListener("click", transformationClicked)
    })

Array.from(document.getElementsByClassName("choice"))
    .forEach((element) => {
        element.addEventListener("click", choiceClicked)
    })

let selected = null;
select(document.getElementById("transformations").children[0]);
let lastChoice = null;

function select(element) {
    if (selected != null) {
        toggleSelectedClass(selected);
    }
    toggleSelectedClass(element);
}

function toggleSelectedClass(element) {
    if (element == null || element == undefined)
        return;
    console.log(element.className);
    let className = "transformation";
    if (element.innerHTML.trim() == "")
        className += " empty-transformation";
    console.log(element.className);
    if (!element.className.endsWith("selected")) {
        className += " selected";
        selected = element;
    }
    
    element.className = className;
}

function transformationClicked(event) {
    let element = event.currentTarget;
    select(element);
}

function choiceClicked(event) {
    if (selected == null)
        return;
    let element = event.currentTarget;
    insertChoice(selected, element);
}

function insertChoice(space, choice) {
    let inIdx = space.getAttribute("data-idx");
    let input = document.getElementById("in-" + inIdx);
    let choiceIdx = choice.getAttribute("data-idx");
    swapHTML(space, choice);
    selectNext(space);
    input.value = choiceIdx;
    lastChoice = choice;
}

function swapHTML(space, choice) {
    if (space.innerHTML.trim() != "") {
        lastChoice.innerHTML = space.innerHTML;
        lastChoice.hidden = false;
    }
    space.innerHTML = choice.innerHTML;
    choice.innerHTML = "";
    choice.hidden = true;
}

function selectNext(element) {
    let transformations = Array.from(document.getElementById("transformations").children);
    let nextTransformation = transformations[transformations.findIndex(e => e === element) + 1];
    select(nextTransformation);
}