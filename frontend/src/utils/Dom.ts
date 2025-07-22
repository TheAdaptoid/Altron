/**
 * Represents an input field element in the DOM,
 * which can be either an HTML input element or a textarea element.
 */
type HTMLInputField = HTMLInputElement | HTMLTextAreaElement;

/**
 * Retrieves an input field element from the DOM by its ID.
 *
 * @param elementId - The ID of the input field element
 * @returns The input field element, or throws an error if the element does not exist or is not an HTMLTextAreaElement or HTMLInputElement.
 */
function getInputField(elementId: string): HTMLInputField {
    // Get the input field element by its ID
    const inputField = document.getElementById(elementId);

    // Check if the input field exists
    if (!inputField) {
        throw new Error(`Input field with ID "${elementId}" not found`);
    }

    // Check if the input field is an HTMLTextAreaElement or HTMLInputElement
    if (
        inputField instanceof HTMLTextAreaElement ||
        inputField instanceof HTMLInputElement
    ) {
        return inputField as HTMLInputField;
    }

    // If not a valid input field, throw an error
    throw new Error(
        'Input field was found but is not an HTMLTextAreaElement or HTMLInputElement'
    );
}

/**
 * Retrieves a select field element from the DOM by its ID.
 *
 * @param elementId - The ID of the select field element
 * @returns The select field element, or throws an error if the element does not exist or is not an HTMLSelectElement.
 */
function getSelectField(elementId: string): HTMLSelectElement {
    // Get the select field element by its ID
    const selectField = document.getElementById(elementId);

    // Check if the select field exists
    if (!selectField) {
        throw new Error(`Select field with ID "${elementId}" not found`);
    }

    // Check if the select field is an HTMLSelectElement
    if (selectField instanceof HTMLSelectElement) {
        return selectField;
    }

    // If not a valid select field, throw an error
    throw new Error('Select field was found but is not an HTMLSelectElement');
}

/**
 * Retrieves a div element from the DOM by its ID.
 *
 * @param elementId - The ID of the div element
 * @returns The div element, or throws an error if the element does not exist.
 */
function getDiv(elementId: string): HTMLDivElement {
    const div = document.getElementById(elementId);
    if (!div) {
        throw new Error(`Div with ID "${elementId}" not found`);
    }
    if (!(div instanceof HTMLDivElement)) {
        throw new Error('Div was found but is not an HTMLDivElement');
    }
    return div;
}

export { getInputField, getSelectField, getDiv };
export type { HTMLInputField };
