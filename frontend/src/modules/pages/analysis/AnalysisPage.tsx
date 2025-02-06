import {Card, Tag, Button, Tabs, Table, Statistic, Row, Col, Space} from "antd";
import {
  DownloadOutlined,
  ShareAltOutlined,
  WarningOutlined,
} from "@ant-design/icons";
import {Line, Column} from "@ant-design/plots";

export const AnalysisPage = () => {
  return (
    <div className="space-y-6">
      <FileHeader />
      <StatisticsOverview />
      <AnomaliesSection />
      <VisualizationsSection />
      <ExportSection />
    </div>
  );
};

const FileHeader = () => (
  <Card>
    <div className="flex justify-between items-center">
      <div className="space-y-2">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold">products_jan2025.csv</h1>
          <Tag color="processing">Processing Complete</Tag>
        </div>
        <p className="text-gray-500">Processed on Jan 15, 2025 10:30 AM</p>
      </div>
      <Button
        type="primary"
        icon={<DownloadOutlined />}
        className="bg-blue-500"
      >
        Download Original
      </Button>
    </div>
  </Card>
);

const StatisticsOverview = () => (
  <Row gutter={[16, 16]}>
    {["Price", "Quantity", "Rating"].map((metric) => (
      <Col span={8} key={metric}>
        <Card title={`${metric} Statistics`}>
          <div className="space-y-4">
            <Statistic
              title="Mean"
              value={245.5}
              precision={2}
              suffix={metric === "Price" ? "€" : ""}
            />
            <Statistic
              title="Median"
              value={230.0}
              precision={2}
              suffix={metric === "Price" ? "€" : ""}
            />
            <Statistic title="Std Dev" value={45.32} precision={2} />
            <div className="h-16">
              <Line
                data={
                  [
                    /* sparkline data */
                  ]
                }
                xField="date"
                yField="value"
                smooth
              />
            </div>
          </div>
        </Card>
      </Col>
    ))}
  </Row>
);

const AnomaliesSection = () => {
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Description",
      dataIndex: "description",
      key: "description",
    },
    {
      title: "Severity",
      dataIndex: "severity",
      key: "severity",
      render: (severity: string) => (
        <Tag
          color={
            severity === "High"
              ? "error"
              : severity === "Medium"
                ? "warning"
                : "success"
          }
        >
          {severity}
        </Tag>
      ),
    },
    {
      title: "Suggested Action",
      dataIndex: "action",
      key: "action",
    },
  ];

  return (
    <Card>
      <Tabs
        items={[
          {
            key: "price",
            label: "Price Anomalies",
            children: <Table columns={columns} />,
          },
          {
            key: "quantity",
            label: "Quantity Anomalies",
            children: <Table columns={columns} />,
          },
          {
            key: "rating",
            label: "Rating Anomalies",
            children: <Table columns={columns} />,
          },
        ]}
      />
    </Card>
  );
};

const VisualizationsSection = () => (
  <Row gutter={[16, 16]}>
    <Col span={12}>
      <Card title="Price Distribution">
        <Column
          data={
            [
              /* distribution data */
            ]
          }
          xField="range"
          yField="count"
        />
      </Card>
    </Col>
    <Col span={12}>
      <Card title="Anomaly Timeline">
        <Line
          data={
            [
              /* timeline data */
            ]
          }
          xField="date"
          yField="anomalies"
        />
      </Card>
    </Col>
  </Row>
);

const ExportSection = () => (
  <Card>
    <Space size="middle">
      <Button type="primary" icon={<DownloadOutlined />}>
        Download Full Report
      </Button>
      <Button icon={<WarningOutlined />}>Export Anomalies</Button>
      <Button icon={<ShareAltOutlined />}>Share Analysis</Button>
    </Space>
  </Card>
);
