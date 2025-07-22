import { ModelType, Model } from '../types/Models';

const BACKEND_HOST: string = 'http://localhost:8000';
const MODELS_ENDPOINT: string = '/api/v1/providers/models';

/**
 * Fetches models from the backend with optional limit and filter.
 *
 * @param {number} [limit] - The maximum number of models to fetch. If not provided, all models are fetched.
 * @param {ModelType} [modelType] - The type filter for the fetched models. If not provided, all models are fetched.
 * @returns {Promise<Model[]>} - A promise resolving to an array of Model objects.
 */
async function fetchModels(limit?: number, modelType?: ModelType): Promise<Model[]> {
    // Build the full URL
    let fullUrl = `${BACKEND_HOST}${MODELS_ENDPOINT}?`;

    // Add limit if provided
    if (limit) {
        fullUrl += `limit=${limit}&`;
    }

    // Add filter if provided
    if (modelType) {
        fullUrl += `model_type=${modelType}&`;
    }

    const response = await fetch(fullUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const data = await response.json();
    return data as Model[];
}

export { fetchModels };
