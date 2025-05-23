"use client";

import { useEffect, useState } from "react";
import { ping_health_endpoint } from "../services/health_check";
import HealthIndicator from "./HealthIndicator";
import type { Status } from "../types/health";

const HEALTH_ENDPOINT = process.env.NEXT_PUBLIC_BACKEND_URL
  ? `${process.env.NEXT_PUBLIC_BACKEND_URL}/health`
  : "http://127.0.0.1:8000/api/v1/health";
const POLLING_INTERVAL = 30000; // Check every 30 seconds

const HealthMonitor = () => {
  const [status, setStatus] = useState<Status>("checking");

  const performHealthCheck = async () => {
    setStatus("checking");
    const isHealthy = await ping_health_endpoint(HEALTH_ENDPOINT);
    setStatus(isHealthy ? "healthy" : "unhealthy");
  };

  useEffect(() => {
    // Initial check
    performHealthCheck();

    // Set up periodic checking
    const interval = setInterval(performHealthCheck, POLLING_INTERVAL);

    // Cleanup on unmount
    return () => clearInterval(interval);
  }, []);

  return <HealthIndicator status={status} />;
};

export default HealthMonitor;
