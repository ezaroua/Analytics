import {
  Card,
  Table,
  DatePicker,
  Input,
  Select,
  Button,
  Row,
  Col,
  Statistic,
  Space,
  Tag,
} from "antd";
import {
  SearchOutlined,
  DeleteOutlined,
  RedoOutlined,
  DownloadOutlined,
} from "@ant-design/icons";

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

const StatisticsPanel = () => (
  <Row gutter={16}>
    <Col span={8}>
      <Card>
        <Statistic
          title="Success Rate"
          value={98.5}
          suffix="%"
          valueStyle={{color: "#3f8600"}}
        />
      </Card>
    </Col>
    <Col span={8}>
      <Card>
        <Statistic title="Average Processing Time" value={2.5} suffix="min" />
      </Card>
    </Col>
    <Col span={8}>
      <Card>
        <Statistic title="Storage Used" value={75} suffix="%" />
      </Card>
    </Col>
  </Row>
);

const HistoryTable = () => {
  const columns = [
    {
      title: "File Name",
      dataIndex: "fileName",
      sorter: true,
    },
    {
      title: "Upload Date",
      dataIndex: "uploadDate",
      sorter: true,
    },
    {
      title: "Status",
      dataIndex: "status",
      render: (status: string) => (
        <Tag
          color={
            status === "Completed"
              ? "success"
              : status === "Processing"
                ? "processing"
                : "error"
          }
        >
          {status}
        </Tag>
      ),
    },
    {
      title: "Anomalies",
      dataIndex: "anomalies",
      render: (count: number) => (
        <Tag color={count > 0 ? "warning" : "success"}>{count}</Tag>
      ),
    },
    {
      title: "Actions",
      key: "actions",
      render: () => (
        <Space>
          <Button type="link">View</Button>
          <Button type="link">Download</Button>
          <Button type="link" danger>
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <Card>
      <div className="mb-4">
        <Space>
          <Button icon={<DownloadOutlined />}>Download Selected</Button>
          <Button icon={<DeleteOutlined />} danger>
            Delete Selected
          </Button>
          <Button icon={<RedoOutlined />}>Reprocess Selected</Button>
        </Space>
      </div>
      <Table
        columns={columns}
        rowSelection={{
          type: "checkbox",
        }}
      />
    </Card>
  );
};
