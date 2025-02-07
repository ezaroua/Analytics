import {SearchOutlined} from "@ant-design/icons";
import {
  Button,
  Card,
  Col,
  DatePicker,
  Input,
  Row,
  Select,
  Space,
  Statistic,
  Table,
  Tag,
} from "antd";
import {useAnalyses} from "../../../shared/hooks/useAnalysis.hook";
import type {
  Analysis,
  AnalysisStatus,
} from "../../../shared/models/analysis.model";

const {RangePicker} = DatePicker;

export const FileHistoryPage = () => {
  return (
    <div className="flex flex-col gap-2">
      <FilterSection />
      <StatisticsPanel />
      <HistoryTable />
    </div>
  );
};

const FilterSection = () => (
  <Card>
    <div className="space-y-4">
      <Row gutter={[16, 16]}>
        <Col span={8}>
          <RangePicker className="w-full" />
        </Col>
        <Col span={6}>
          <Select
            placeholder="Status"
            className="w-full"
            options={[
              {value: "completed", label: "Completed"},
              {value: "processing", label: "Processing"},
              {value: "failed", label: "Failed"},
            ]}
          />
        </Col>
        <Col span={6}>
          <Select
            placeholder="Anomaly Type"
            className="w-full"
            mode="multiple"
            options={[
              {value: "price", label: "Price"},
              {value: "quantity", label: "Quantity"},
              {value: "rating", label: "Rating"},
            ]}
          />
        </Col>
        <Col span={4}>
          <Input placeholder="Search files" prefix={<SearchOutlined />} />
        </Col>
      </Row>
    </div>
  </Card>
);

const HistoryTable = () => {
  const {data, isLoading, error} = useAnalyses();

  const columns = [
    {
      title: "File ID",
      dataIndex: "fileId",
    },
    {
      title: "File Name",
      dataIndex: ["metadata", "filename"],
    },
    {
      title: "Status",
      dataIndex: "status",
      render: (status: AnalysisStatus) => (
        <Tag
          color={
            status === "COMPLETED"
              ? "success"
              : status === "PROCESSING"
                ? "processing"
                : status === "PENDING"
                  ? "default"
                  : "error"
          }
        >
          {status}
        </Tag>
      ),
    },
    {
      title: "Anomalies",
      dataIndex: "anomaly_count",
      render: (count: number) => (
        <Tag color={count > 0 ? "warning" : "success"}>{count}</Tag>
      ),
    },
    {
      title: "Actions",
      key: "actions",
      render: (_: any, record: Analysis) => (
        <Space>
          <Button type="link" href={`/analysis/${record.fileId}`}>
            View
          </Button>
          <Button type="link" danger>
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  if (error) {
    return (
      <Card>
        <div className="text-red-500">
          Error loading analyses: {error.message}
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <Table
        columns={columns}
        dataSource={data?.items}
        rowKey="fileId"
        loading={isLoading}
        rowSelection={{type: "checkbox"}}
      />
    </Card>
  );
};

// Update StatisticsPanel to use real data
const StatisticsPanel = () => {
  const {data} = useAnalyses();

  const getSuccessRate = () => {
    if (!data?.items.length) {
      return 0;
    }
    const completed = data.items.filter(
      (item) => item.status === "COMPLETED"
    ).length;
    return ((completed / data.items.length) * 100).toFixed(1);
  };

  return (
    <Row gutter={16}>
      <Col span={8}>
        <Card>
          <Statistic
            title="Success Rate"
            value={getSuccessRate()}
            suffix="%"
            valueStyle={{color: "#3f8600"}}
          />
        </Card>
      </Col>
      <Col span={8}>
        <Card>
          <Statistic title="Total Files" value={data?.items.length ?? 0} />
        </Card>
      </Col>
    </Row>
  );
};
