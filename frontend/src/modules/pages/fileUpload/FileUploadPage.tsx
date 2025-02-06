import {
  FileTextOutlined,
  InboxOutlined,
  LoadingOutlined,
} from "@ant-design/icons";
import { Alert, Card, Col, Progress, Row, Typography, Upload } from "antd";
import { useState } from "react";
import { useFileUpload } from "../../../shared/hooks/useAnalysis.hook";
import { StatsCard } from "../dashboard/StatCard";

const { Title, Text } = Typography;
const { Dragger } = Upload;

export const FileUploadPage = () => {
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const uploadMutation = useFileUpload();

  const handleUpload = async (file: File) => {
    console.log("Uploading file:", file);
    setSelectedFile(file);
    try {
      await uploadMutation.mutateAsync({
        file,
        onProgress: setUploadProgress,
      });
      setSelectedFile(null);
      setUploadProgress(0);
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      setUploadProgress(0);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center space-y-2">
        <Title level={2}>Upload CSV File</Title>
        <Text type="secondary">
          Upload your CSV file containing product data for analysis
        </Text>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <StatsCard
            title="Files Processed Today"
            value={12}
            prefix={<FileTextOutlined />}
          />
        </Col>
        <Col span={8}>
          <StatsCard title="Success Rate" value={98.5} suffix="%" />
        </Col>
        <Col span={8}>
          <StatsCard title="Average Process Time" value={2.5} suffix="min" />
        </Col>
      </Row>

      <Card className="shadow-sm hover:shadow-md transition-shadow flex flex-col gap-4">
        <Dragger
          beforeUpload={async (file) => {
            await handleUpload(file);
            return false;
          }}
          accept=".csv"
          showUploadList={false}
          disabled={uploadMutation.isPending}
        >
          <div className="p-8 space-y-4">
            {uploadMutation.isPending ? (
              <LoadingOutlined className="text-4xl text-blue-500" />
            ) : (
              <InboxOutlined className="text-4xl text-blue-500" />
            )}
            <div>
              <p className="text-lg font-medium">
                {uploadMutation.isPending
                  ? "Uploading..."
                  : "Drop CSV file here"}
              </p>
              <p className="text-gray-500">
                or <span className="text-blue-500">browse files</span>
              </p>
            </div>
          </div>
        </Dragger>

        {selectedFile && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <FileTextOutlined />
              <Text strong>{selectedFile.name}</Text>
              <Text type="secondary">
                ({(selectedFile.size / 1024).toFixed(2)} KB)
              </Text>
            </div>
            {uploadProgress > 0 && (
              <Progress
                percent={Math.round(uploadProgress)}
                status={uploadProgress === 100 ? "success" : "active"}
                strokeColor={{
                  "0%": "#108ee9",
                  "100%": "#87d068",
                }}
                className="mt-2"
              />
            )}
          </div>
        )}

        {uploadMutation.isError && (
          <Alert
            message="Upload Failed"
            description="There was an error uploading your file. Please try again."
            type="error"
            showIcon
            className="mt-4"
          />
        )}

        {uploadMutation.isSuccess && (
          <Alert
            message="Upload Successful"
            description="Your file has been uploaded and is being analyzed."
            type="success"
            showIcon
            className="mt-4"
          />
        )}
      </Card>

      <Card title="File Requirements" className="bg-gray-50">
        <div className="space-y-2">
          <Text>Your CSV file should include:</Text>
          <ul className="list-disc list-inside text-gray-600">
            <li>Product ID (unique identifier)</li>
            <li>Product Name</li>
            <li>Price (between 10€ and 500€)</li>
            <li>Quantity (between 1 and 50 units)</li>
            <li>Customer Rating (between 1.0 and 5.0)</li>
          </ul>
        </div>
      </Card>
    </div>
  );
};
