import React from 'react';
import { UserMessage, MessageThread, AssistantMessage } from '../types/Messages';
import { getInputField, HTMLInputField, getSelectField } from '../utils/Dom';
import { fetchModels } from '../logic/Models';
import { Model, ModelType } from '../types/Models';
import '../styles/UserInputContainer.css';

const USER_INPUT_FIELD_ID = 'userInputField';

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
    if (!input || input.trim() === '') {
        console.warn('Input is empty or invalid');
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
 * @param setMessageThread - The message thread to submit the message to.
 */
async function submitHandler(
    messageThread: MessageThread,
    setMessageThread: React.Dispatch<React.SetStateAction<MessageThread>>
) {
    // Get the input field and submit the user message
    const inputField: HTMLInputField = getInputField('userInputField');

    // Validate the input before submitting
    if (!validateInput(inputField.value)) {
        return;
    }

    // Get the user input and clear the input field
    const userInput: string = inputField.value.trim();
    inputField.value = ''; // Clear the input field after submission

    // Create a user message object
    const userMessage: UserMessage = new UserMessage(userInput);
    const agentMessage: AssistantMessage = new AssistantMessage('Echo: ' + userInput);

    // Add the user message to the message thread
    const updatedThread: MessageThread = {
        ...messageThread,
        messages: [...messageThread.messages, userMessage, agentMessage],
    };
    setMessageThread(updatedThread);
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
async function KeyDownHandler(
    event: React.KeyboardEvent<HTMLTextAreaElement>,
    messageThread: MessageThread,
    setMessageThread: React.Dispatch<React.SetStateAction<MessageThread>>
) {
    if (event.key === 'Enter' && event.shiftKey) {
        // Insert a new line into the input field
        event.preventDefault();
        const inputField: HTMLInputField = getInputField(USER_INPUT_FIELD_ID);
        inputField.value += '\n';
    } else if (event.key === 'Tab') {
        // Insert a tab character into the input field
        event.preventDefault();
        const inputField: HTMLInputField = getInputField(USER_INPUT_FIELD_ID);
        inputField.value += '\t';
    } else if (event.key === 'Enter') {
        // Submit the input when Enter is pressed
        event.preventDefault();
        await submitHandler(messageThread, setMessageThread);
    }
}

/**
 * Loads chat models from the server and populates the model select field.
 *
 * This function is called in a useEffect hook and checks if models are already loaded.
 * If so, it does nothing and returns.
 * If not, it fetches the models from the server and populates the select field.
 * The state is updated to indicate that models are loaded.
 *
 * @param modelsLoaded - A boolean indicating if models are already loaded.
 * @param setModelsLoaded - A function to update the state of modelsLoaded.
 */
async function LoadModels(
    selectedModel: Model | null,
    setSelectedModel: React.Dispatch<React.SetStateAction<Model | null>>,
    setAvailableModels: React.Dispatch<React.SetStateAction<Model[]>>
) {
    // Check if models are already loaded
    if (selectedModel !== null) {
        console.log('Models are already loaded. No new models fetched.');
        return; // If so, return
    }

    // Fetch models
    const modelList: Model[] = await fetchModels(undefined, ModelType.Chat);

    // Get the select field
    const modelSelect: HTMLSelectElement = getSelectField('modelSelect');

    // Clear existing options
    modelSelect.innerHTML = '';

    // Populate the select field with model options
    modelList.forEach((model) => {
        const option = document.createElement('option');
        option.value = model.id;
        option.textContent = model.alias || model.id;
        modelSelect.appendChild(option);
    });

    // Update state
    setSelectedModel(modelList[0]);
    setAvailableModels(modelList);
    console.log('Models loaded successfully.');
}

/**
 * Handles changes to the model select field.
 *
 * When a model is selected in the select field, this function finds the
 * corresponding model in the list of available models and updates the state
 * with the selected model. If the selected model is not found, an error is thrown.
 *
 * @param event - The change event.
 * @param availableModels - The list of available models.
 * @param setSelectedModel - The function to update the state with the selected model.
 */
async function ModelSelectHandler(
    event: React.ChangeEvent<HTMLSelectElement>,
    availableModels: Model[],
    setSelectedModel: React.Dispatch<React.SetStateAction<Model | null>>
) {
    const selectedModelId: string = event.target.value;
    const modelIds: string[] = availableModels.map((model) => model.id);

    if (modelIds.includes(selectedModelId)) {
        // Find the selected model
        const selectedModel: Model | undefined = availableModels.find(
            (model) => model.id === selectedModelId
        );

        // Update state
        if (selectedModel !== undefined) {
            setSelectedModel(selectedModel);
        } else {
            throw new Error('Selected model not found');
        }
    }
}

/**
 * The UserInputContainer component provides an input field for the user to type a message
 * and a select field for selecting a model. The component also provides a button to attach
 * a file and a button to submit the message.
 *
 * The component loads the list of available models when the component mounts and stores
 * the list in state. When the selected model is changed, the component updates the state
 * with the selected model.
 *
 * The component also handles key down events on the input field. The Enter key is handled
 * to submit the message and the Tab key is handled to insert a tab character.
 *
 * @param messageThread - The message thread to submit the message to.
 * @param setMessageThread - The function to update the state with the submitted message.
 * @param selectedModel - The currently selected model.
 * @param setSelectedModel - The function to update the state with the selected model.
 */
function UserInputContainer({
    messageThread,
    setMessageThread,
    selectedModel,
    setSelectedModel,
}: {
    messageThread: MessageThread;
    setMessageThread: React.Dispatch<React.SetStateAction<MessageThread>>;
    selectedModel: Model | null;
    setSelectedModel: React.Dispatch<React.SetStateAction<Model | null>>;
}) {
    // State to hold available models
    const [availableModels, setAvailableModels] = React.useState<Model[]>([]);

    // Load models
    React.useEffect(() => {
        if (selectedModel === null) {
            LoadModels(selectedModel, setSelectedModel, setAvailableModels);
        }
    }, [selectedModel, setSelectedModel, setAvailableModels]);

    return (
        <div className="UserInputContainer">
            <textarea
                id={USER_INPUT_FIELD_ID}
                className="UserInputField"
                placeholder="Type here..."
                onKeyDown={async (event) =>
                    await KeyDownHandler(event, messageThread, setMessageThread)
                }
            />
            <div className="OptionDiv">
                <select
                    id="modelSelect"
                    onChange={async (event) =>
                        await ModelSelectHandler(
                            event,
                            availableModels,
                            setSelectedModel
                        )
                    }
                >
                    <option value="Null">Loading Models...</option>
                </select>
                <button>Attach File</button>
                <button
                    onClick={async () =>
                        await submitHandler(messageThread, setMessageThread)
                    }
                >
                    Submit
                </button>
            </div>
        </div>
    );
}

export default UserInputContainer;
