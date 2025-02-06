import {Card, Progress, Space, Typography} from "antd";

const {Text} = Typography;

export const SystemStatus = () => {
  return (
    <Card title="System Status" className="h-full">
      <Space direction="vertical" className="w-full">
        <div>
          <div className="flex justify-between mb-2">
            <Text>Storage Usage</Text>
            <Text>75%</Text>
          </div>
          <Progress percent={75} showInfo={false} />
        </div>
        <div>
          <div className="flex justify-between mb-2">
            <Text>Processing Queue</Text>
            <Text>3 files</Text>
          </div>
          <Progress percent={30} showInfo={false} />
        </div>
        <div>
          <div className="flex justify-between mb-2">
            <Text>System Load</Text>
            <Text>45%</Text>
          </div>
          <Progress percent={45} showInfo={false} />
        </div>
      </Space>
    </Card>
  );
};
