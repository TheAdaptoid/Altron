import { type Status } from "../types/health";

interface HealthIndicatorProps {
  status: Status;
}

const HealthIndicator = ({ status }: HealthIndicatorProps) => {
  const getColor = () => {
    switch (status) {
      case "checking":
        return "bg-yellow-500";
      case "healthy":
        return "bg-green-500";
      case "unhealthy":
        return "bg-red-500";
    }
  };

  return (
    <div className="fixed bottom-4 right-4 flex items-center gap-2">
      <div
        className={`w-4 h-4 rounded-full ${getColor()} transition-colors duration-300`}
        title={`Status: ${status}`}
      />
      <span className="text-sm text-gray-600">{status}</span>
    </div>
  );
};

export default HealthIndicator;
