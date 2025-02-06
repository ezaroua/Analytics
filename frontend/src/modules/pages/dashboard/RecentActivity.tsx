import {Card, List, Tag, Typography} from "antd";
import {Link} from "react-router-dom";

const {Text} = Typography;

interface RecentFile {
  id: string;
  name: string;
  status: "success" | "processing" | "error";
  timestamp: string;
  anomalies: number;
}

export const RecentActivity = () => {
  const recentFiles: RecentFile[] = [
    {
      id: "1",
      name: "products-jan-2025.csv",
      status: "success",
      timestamp: "2025-01-15T10:30:00",
      anomalies: 5,
    },
    // Add more mock data
  ];

  const getStatusTag = (status: RecentFile["status"]) => {
    const config = {
      success: {color: "success", text: "Completed"},
      processing: {color: "processing", text: "Processing"},
      error: {color: "error", text: "Failed"},
    };
    return <Tag color={config[status].color}>{config[status].text}</Tag>;
  };

  return (
    <Card title="Recent Activity" className="h-full">
      <List
        dataSource={recentFiles}
        renderItem={(item) => (
          <List.Item
            // biome-ignore lint/correctness/useJsxKeyInIterable: <explanation>
            actions={[<Link to={`/analysis/${item.id}`}>View Details</Link>]}
          >
            <List.Item.Meta
              title={item.name}
              description={
                <div className="space-y-1">
                  <div>{getStatusTag(item.status)}</div>
                  <Text type="secondary">
                    {new Date(item.timestamp).toLocaleString()}
                  </Text>
                </div>
              }
            />
            {item.anomalies > 0 && (
              <Tag color="warning">{item.anomalies} anomalies</Tag>
            )}
          </List.Item>
        )}
      />
    </Card>
  );
};
