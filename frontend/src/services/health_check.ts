/**
 * This function pings a health endpoint and checks if it is healthy
 * by verifying if the response status code is 200.
 *
 * @param endpoint - The health endpoint to ping
 * @returns A promise that resolves to true if the endpoint is healthy (status code 200), false otherwise
 */
export async function ping_health_endpoint(endpoint: string): Promise<boolean> {
  try {
    // Make a GET request to the health endpoint
    const response = await fetch(endpoint, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Return true if the response is OK (status code 200)
    return response.ok;
  } catch (error) {
    // Handle any errors that occur during the fetch
    console.error("Error pinging health endpoint:", error);
    return false;
  }
}
