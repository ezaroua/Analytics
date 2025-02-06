import {
  DeleteOutlined,
  DownloadOutlined,
  RedoOutlined,
} from "@ant-design/icons";
import {
  Button,
  Card,
  Space,
  Table,
  Tag
} from "antd";
import { useEffect, useState } from "react";

interface ProductError {
  ID: number;
  Nom: string;
  Prix: number;
  Quantite: number;
  Note_Client: number;
  error_message: string;
}

const mockData = {
  products_on_error: [
    {
      ID: 1,
      Nom: "Produit_1",
      Prix: 193.52,
      Quantite: 32,
      Note_Client: 1.1,
      error_message: "Invalid value type 1",
    },
    {
      ID: 3,
      Nom: "Produit_3",
      Prix: 368.68,
      Quantite: 49,
      Note_Client: 1.9,
      error_message: "Invalid value type 3",
    },
    {
      ID: 5,
      Nom: "Produit_5",
      Prix: 86.45,
      Quantite: 4,
      Note_Client: 1.7,
      error_message: "Invalid value type 5",
    },
  ],
};

const HistoryTable = () => {
  const [data, setData] = useState<ProductError[]>([]);

  useEffect(() => {
    setData(mockData.products_on_error);
  }, []);

  const columns = [
    {
      title: "ID",
      dataIndex: "ID",
      key: "ID",
    },
    {
      title: "Nom",
      dataIndex: "Nom",
      key: "Nom",
    },
    {
      title: "Prix",
      dataIndex: "Prix",
      key: "Prix",
      render: (price: number) => `€${price.toFixed(2)}`,
    },
    {
      title: "Quantité",
      dataIndex: "Quantite",
      key: "Quantite",
    },
    {
      title: "Note Client",
      dataIndex: "Note_Client",
      key: "Note_Client",
      render: (note: number) => <Tag color={note < 2 ? "orange" : "green"}>{note}</Tag>,
    },
    {
      title: "Erreur",
      dataIndex: "error_message",
      key: "error_message",
      render: (msg: string) => <Tag color="red">{msg}</Tag>,
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
      <Table columns={columns} dataSource={data} rowKey="ID" />
    </Card>
  );
};

export default HistoryTable;
