import React from "react";
import "../styles/UserInputContainer.css";
import { Message, MessageThread } from "../logic/converse";
/**
 * Retrieves the input field element with the ID "userInputField" from the DOM.
 *
 * @returns {HTMLTextAreaElement} The input field element.
 * @throws {Error} If the element is not found or is not an HTMLTextAreaElement.
 */
function getInputField(): HTMLTextAreaElement {
    // Get the input field element by its ID
    const inputField = document.getElementById("userInputField");
    // Check if the input field exists and is an HTMLTextAreaElement
    if (inputField && inputField instanceof HTMLTextAreaElement) {
        return inputField;
    }
    // If not found or not an HTMLTextAreaElement, throw an error
    throw new Error("Input field not found or is not an HTMLTextAreaElement");
}

function submitHandler() {
    // Get the input field value
    const inputField: HTMLTextAreaElement = getInputField();

    // Get the value from the input field
    const inputValue: string = inputField.value.trim();
    inputField.value = ""; // Clear the input field after submission

    // Check if the input value is empty
    if (inputValue === "") {
        console.warn("Input field is empty");
        return;
    }

    // Log the input value to the console
    console.log("User input submitted:", inputValue);
}

function KeyDownHandler(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    // Insert a new line into the input field
    if (event.key === "Enter" && event.shiftKey) {
        event.preventDefault();
        const inputField: HTMLTextAreaElement = getInputField();
        inputField.value += "\n";

        // Insert a tab character into the input field
    } else if (event.key === "Tab") {
        event.preventDefault();
        const inputField: HTMLTextAreaElement = getInputField();
        inputField.value += "\t";

        // Submit the input when Enter is pressed
    } else if (event.key === "Enter") {
        event.preventDefault();
        submitHandler();
    }
}

function UserInputContainer({ messageThread }: { messageThread: MessageThread }) {
    
    return (
        <div className="UserInputContainer">
            <textarea
                id="userInputField"
                className="UserInputField"
                placeholder="Type here..."
                onKeyDown={KeyDownHandler}
            />
            <button onClick={submitHandler}>/\</button>
        </div>
    );
}

export default UserInputContainer;
