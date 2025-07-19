import React from "react";
import "../styles/UserInputContainer.css";
import { UserMessage, MessageThread } from "../types/Messages";
import { getInputField, HTMLInputField, getSelectField } from "../utils/Dom";
import { submitUserMessage } from "../logic/converse";
import { fetchModels } from "../logic/Models";
import { Model, ModelType } from "../types/Models";

const USER_INPUT_FIELD_ID = "userInputField";

/**
 * Validates user input before submitting a message.
 *
 * Checks if the input is empty or contains only whitespace.
 * Returns false if the input is invalid, true otherwise.
 * Additional validation logic can be added here.
 *
 * @param input - The user input string to validate.
 * @returns {boolean} - True if the input is valid, false otherwise.
 */
function validateInput(input: string): boolean {
    // Check if the input is empty or contains only whitespace
    if (!input || input.trim() === "") {
        console.warn("Input is empty or invalid");
        return false;
    }
    // Additional validation logic can be added here
    return true;
}

/**
 * Submits a user message to the message thread.
 *
 * Gets the input field, validates the user input, clears the input field,
 * creates a user message object, and submits the message to the message thread.
 *
 * @param messageThread - The message thread to submit the message to.
 */
async function submitHandler(messageThread: MessageThread) {
    // Get the input field and submit the user message
    const inputField: HTMLInputField = getInputField("userInputField");

    // Validate the input before submitting
    if (!validateInput(inputField.value)) {
        return;
    }

    // Get the user input and clear the input field
    const userInput: string = inputField.value.trim();
    inputField.value = ""; // Clear the input field after submission

    // Create a user message object
    const userMessage: UserMessage = {
        id: crypto.randomUUID(),
        content: userInput,
        role: "user",
    };

    // Submit the user message
    await submitUserMessage(userMessage, messageThread);
}

/**
 * Handles key down events on the user input field.
 *
 * The following keys are handled:
 * - Enter + Shift: Insert a new line into the input field.
 * - Tab: Insert a tab character into the input field.
 * - Enter: Submit the user message.
 *
 * @param event - The keyboard event.
 * @param messageThread - The message thread to submit the message to.
 */
function KeyDownHandler(
    event: React.KeyboardEvent<HTMLTextAreaElement>,
    messageThread: MessageThread
) {
    if (event.key === "Enter" && event.shiftKey) {
        // Insert a new line into the input field
        event.preventDefault();
        const inputField: HTMLInputField = getInputField(USER_INPUT_FIELD_ID);
        inputField.value += "\n";
    } else if (event.key === "Tab") {
        // Insert a tab character into the input field
        event.preventDefault();
        const inputField: HTMLInputField = getInputField(USER_INPUT_FIELD_ID);
        inputField.value += "\t";
    } else if (event.key === "Enter") {
        // Submit the input when Enter is pressed
        event.preventDefault();
        submitHandler(messageThread);
    }
}

async function LoadModels(modelsLoaded: boolean, setModelsLoaded: React.Dispatch<React.SetStateAction<boolean>>) {
    // Check if models are already loaded
    if (modelsLoaded) {
        console.log("Models are already loaded. No new models fetched.");
        return; // If so, return
    }    
    
    // Simulate a delay for fetching models
    const modelList: Model[] = await fetchModels(
        undefined,
        ModelType.Chat
    );

    // Get the select field
    const modelSelect: HTMLSelectElement = getSelectField("modelSelect");

    // Clear existing options
    modelSelect.innerHTML = "";

    // Populate the select field with model options
    modelList.forEach((model) => {
        const option = document.createElement("option");
        option.value = model.id;
        option.textContent = model.alias || model.id;
        modelSelect.appendChild(option);
    });

    // Update the state to indicate models are loaded
    setModelsLoaded(true);
    console.log("Models loaded successfully.");
}

function UserInputContainer({ messageThread }: { messageThread: MessageThread }) {
    // State to track if models have already been loaded
    const [modelsLoaded, setModelsLoaded] = React.useState(false);
    
    return (
        <div className="UserInputContainer">
            <textarea
                id={USER_INPUT_FIELD_ID}
                className="UserInputField"
                placeholder="Type here..."
                onKeyDown={(event) => KeyDownHandler(event, messageThread)}
            />
            <div className="OptionDiv">
                <button>Attach File</button>
                <select id="modelSelect" onFocus={() => LoadModels(modelsLoaded, setModelsLoaded)}>
                    <option value="Null">Loading Models...</option>
                </select>
                <button onClick={() => submitHandler(messageThread)}>Submit</button>
            </div>
        </div>
    );
}

export default UserInputContainer;
