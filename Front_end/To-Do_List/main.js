let todoInput = document.querySelector(".todo-input");
let todoButton = document.querySelector(".todo-button");
let taskList = document.querySelector("#task-list")

//Function when button task is clicked
todoButton.addEventListener("click", function (e) {
    e.preventDefault(); // no reloading with form
    saveLocal(todoInput.value)
    createTaskLine(todoInput.value)

});

taskList.addEventListener("click", function (e) { // When the Ul list zone is clicked
    let item = e.target; // the target is set on the clicked element

    if (item.className === "delete-btn") {
        parent = item.parentElement;
        removeLocal(parent);
        parent.remove()
    }

    if (item.classList[0] === "check") {
        let text = item.nextSibling;
        console.log(text.classList)
        text.classList.toggle("completed")
    }
});

// Function to save element on LocalStorage
function saveLocal(elem) {
    let tasks;
    if (localStorage.getItem("tasks") === null) {
        tasks = [];
    } else {
        tasks = JSON.parse(localStorage.getItem("tasks"));
    }
    tasks.push(elem);
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

// Function to remove an element on the LocalStorage
function removeLocal(elem) {
    let tasks;
    if (localStorage.getItem("tasks") === null) {
        tasks = [];
    } else {
        tasks = JSON.parse(localStorage.getItem("tasks"));
    }
    const todoIndex = elem.children[0].innerText;
    tasks.splice(tasks.indexOf(todoIndex), 1);
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

// Create all elements for a task line
function createTaskLine(inputValue) {
    let taskToDo = document.createElement("li");

    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "check";
    taskToDo.appendChild(checkbox);

    let taskText = document.createElement("span");
    taskText.innerText = inputValue;
    taskText.className = "task";
    taskToDo.appendChild(taskText);
    todoInput.value = "";

    let delButton = document.createElement("button");
    delButton.type = "button";
    delButton.innerText = "x";
    delButton.className = "delete-btn";
    taskToDo.appendChild(delButton);

    taskList.appendChild(taskToDo);
}

// Load the same number of tasks and name them with the array in LocalStorage
document.addEventListener("DOMContentLoaded", function () {
    let tasks;
    if (localStorage.getItem("tasks") === null) {
        tasks = [];
    } else {
        tasks = JSON.parse(localStorage.getItem("tasks"));
    }
    tasks.forEach(function (todo) {
        createTaskLine(todo)
    });
});
