import { ModelType, Model } from "../types/Models";

const BACKEND_HOST: string = "http://localhost:8000";
const MODELS_ENDPOINT: string = "/api/v1/providers/models"

async function fetchModels(limit?:number, filter?: ModelType): Promise<Model[]> {
    // Build the full URL
    let fullUrl = `${BACKEND_HOST}${MODELS_ENDPOINT}?`;

    // Add limit if provided
    if (limit) {
        fullUrl += `limit=${limit}&`;
    }

    // Add filter if provided
    if (filter) {
        fullUrl += `type_filter=${filter}&`;
    }

    const response = await fetch(fullUrl, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    const data = await response.json();
    return data as Model[];    
}

export { fetchModels };