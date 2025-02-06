import {Row, Col} from "antd";
import {
  FileOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined,
  SyncOutlined,
} from "@ant-design/icons";
import {StatsCard} from "./StatCard";

export const AnalysisOverview = () => {
  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={6}>
        <StatsCard
          title="Total Files"
          value={134}
          prefix={<FileOutlined />}
          trend={12}
        />
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <StatsCard
          title="In Progress"
          value={3}
          prefix={<SyncOutlined spin />}
        />
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <StatsCard
          title="Failed"
          value={2}
          prefix={<ExclamationCircleOutlined />}
          trend={-50}
        />
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <StatsCard
          title="Success Rate"
          value={96.5}
          prefix={<CheckCircleOutlined />}
          suffix="%"
        />
      </Col>
    </Row>
  );
};
