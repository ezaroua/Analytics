import {Row, Col} from "antd";
import {AnalysisOverview} from "./AnalysisOverview";
import {AnomaliesSummary} from "./AnomaliesSummary";
import {RecentActivity} from "./RecentActivity";
import {SystemStatus} from "./SystemStatus";

export const Dashboard = () => {
  return (
    <div className="space-y-6">
      <AnalysisOverview />

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <AnomaliesSummary />
        </Col>
        <Col xs={24} lg={12}>
          <RecentActivity />
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={24}>
          <SystemStatus />
        </Col>
      </Row>
    </div>
  );
};
