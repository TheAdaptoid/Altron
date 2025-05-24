import axios from "axios";
import { HEALTH_URL } from "./constants";

function check_connection(url: string): Promise<boolean> {
  return axios
    .get(url)
    .then((response) => {
      // Check if the response is successful
      if (response.status === 200) {
        return true;
      } else {
        console.error("Connection failed with status:", response.status);
        return false;
      }
    })
    .catch((error) => {
      console.error("Connection error:", error);
      return false;
    });
}

async function update_connection_indicator(): Promise<void> {
  // Get the connection indicator element
  const connectionIndicator = document.getElementById(
    "connection-indicator"
  ) as HTMLDivElement;

  // If the connection indicator is not found,
  // then log an error and return
  if (!connectionIndicator) {
    console.error("Connection indicator element not found");
    return;
  }

  // Clear the existing content
  connectionIndicator.innerHTML = "Connecting...";
  connectionIndicator.style.color = "orange";

  // Pause for 1 second
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Check the connection to the server
  const isConnected = await check_connection(HEALTH_URL);

  // Update the connection indicator based on the connection status
  if (isConnected) {
    connectionIndicator.innerHTML = "Connected";
    connectionIndicator.style.color = "green";
  } else {
    connectionIndicator.innerHTML = "Disconnected";
    connectionIndicator.style.color = "red";
  }
}

// Call the function to update the model selector
while (true) {
  await update_connection_indicator();
  // Wait for 10 seconds before checking again
  await new Promise((resolve) => setTimeout(resolve, 10000));
}
