import {Card, Form, Input, Select, Checkbox, Switch, Button} from "antd";

export const NotificationSettingsPage = () => {
  return (
    <div className="flex flex-col max-w-4xl mx-auto gap-2">
      <EmailSettings />
      <PushSettings />
      <NotificationHistory />
    </div>
  );
};

const EmailSettings = () => (
  <Card title="Email Notifications">
    <Form layout="vertical">
      <Form.Item label="Email Address">
        <Input type="email" />
      </Form.Item>
      <Form.Item label="Notification Frequency">
        <Select
          options={[
            {value: "immediate", label: "Immediate"},
            {value: "daily", label: "Daily Digest"},
            {value: "weekly", label: "Weekly Summary"},
          ]}
        />
      </Form.Item>
      <Form.Item label="Notification Types">
        <Checkbox.Group
          options={[
            {label: "Upload Complete", value: "upload"},
            {label: "Analysis Complete", value: "analysis"},
            {label: "Critical Anomalies", value: "anomalies"},
          ]}
        />
      </Form.Item>
      <Button type="primary">Send Test Email</Button>
    </Form>
  </Card>
);

const PushSettings = () => (
  <Card title="Push Notifications">
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <span>Enable Push Notifications</span>
        <Switch />
      </div>
      <div className="bg-gray-50 p-4 rounded">
        <p className="text-sm text-gray-600">
          Browser notifications are currently enabled
        </p>
      </div>
      <Checkbox.Group
        className="w-full"
        options={[
          {label: "Upload Notifications", value: "upload"},
          {label: "Analysis Notifications", value: "analysis"},
          {label: "System Notifications", value: "system"},
        ]}
      />
    </div>
  </Card>
);

const NotificationHistory = () => (
  <Card title="Recent Notifications">
    {/* <List
      dataSource={[notificationData]}
      renderItem={(item: unknown) => (
        // TODO: Type this after I finish with AWS
        <List.Item
          extra={
            <Badge
              status={item.read ? 'default' : 'processing'}
              text={item.read ? 'Read' : 'Unread'}
            />
          }
        >
          <List.Item.Meta
            avatar={<BellOutlined />}
            title={item.title}
            description={item.timestamp}
          />
        </List.Item>
      )}
    /> */}
  </Card>
);
