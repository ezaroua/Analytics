import {Layout, Menu} from "antd";
import {Outlet, useNavigate, useLocation} from "react-router-dom";
import {
  DashboardOutlined,
  UploadOutlined,
  HistoryOutlined,
  BellOutlined,
} from "@ant-design/icons";
import { ROUTE_PATH } from "../../../shared/routes";
import { PageHeader } from "../../components/PageHeader";

const {Header, Sider, Content} = Layout;

export const DashboardLayout = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: ROUTE_PATH.public.DASHBOARD,
      icon: <DashboardOutlined />,
      label: "Dashboard",
    },
    {
      key: ROUTE_PATH.public.FILE_UPLOAD,
      icon: <UploadOutlined />,
      label: "Upload",
    },
    {
      key: ROUTE_PATH.public.HISTORY,
      icon: <HistoryOutlined />,
      label: "History",
    },
    {
      key: ROUTE_PATH.public.NOTIFICATIONS,
      icon: <BellOutlined />,
      label: "Notifications",
    },
  ];

  return (
    <Layout className="min-h-screen">
      <Sider breakpoint="lg" collapsedWidth="0">
        <div className="h-16 flex items-center justify-center">
          <h1 className="text-white text-xl">CSV Analyzer</h1>
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({key}) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header className="bg-white px-4 flex items-center justify-between">
          <PageHeader />
          <div className="flex items-center gap-4">
            {/* Add user profile, etc */}
          </div>
        </Header>
        <Content className="m-6">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};
