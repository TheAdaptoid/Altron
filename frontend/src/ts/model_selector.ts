import axios from "axios";
import { MODELS_URL } from "./constants";

interface ModelDetails {
  id: string;
  //   modelType: string;
  //   status: string;
}

async function get_available_models(): Promise<ModelDetails[]> {
  try {
    const response = await axios.get<ModelDetails[]>(MODELS_URL);

    // Check if the response is an array
    if (!Array.isArray(response.data)) {
      console.error(
        "Invalid response format. Expected an array. Got:",
        typeof response.data,
        `${response.data}`
      );
      return [];
    }

    return response.data;
  } catch (error) {
    console.error("Error fetching models:", error);
    return [];
  }
}

async function update_model_selector(): Promise<void> {
  // Get the model selector element
  const modelSelector = document.getElementById(
    "model-selector"
  ) as HTMLSelectElement;

  // If the model selector is not found,
  // then log an error and return
  if (!modelSelector) {
    console.error("Model selector element not found");
    return;
  }

  // Clear the existing options
  modelSelector.innerHTML = "";

  // Fetch the available models
  const models = await get_available_models();

  // Populate the model selector with the available models
  models.forEach((model) => {
    // Create a new option element
    const option = document.createElement("option");
    option.value = model.id;
    option.textContent = `${model.id}`;

    // Append the option to the model selector
    modelSelector.appendChild(option);
  });
}

// Function to handle model selection
// async function handle_model_selection(): Promise<void> {}

update_model_selector();
