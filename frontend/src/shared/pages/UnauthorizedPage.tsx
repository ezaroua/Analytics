import {
  ContactsOutlined,
  HomeOutlined,
  LockOutlined,
  RollbackOutlined,
} from "@ant-design/icons";
import {Button, Typography} from "antd";
import {useNavigate} from "react-router-dom";

const {Title, Text, Link} = Typography;

const UnauthorizedPage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gradient-to-b from-red-50 to-white">
      <div className="relative w-full max-w-3xl space-y-8 text-center">
        {/* Background Pattern */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute inset-0 opacity-30">
            {[...Array(10)].map((_, i) => (
              <div
                // biome-ignore lint/suspicious/noArrayIndexKey: <explanation>
                key={i}
                className="absolute"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                  transform: `rotate(${Math.random() * 360}deg)`,
                }}
              >
                <LockOutlined
                  className="text-red-300"
                  style={{fontSize: `${Math.random() * 20 + 10}px`}}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Error Number */}
          <div className="relative">
            <Title
              className="m-0 font-bold text-red-100 select-none text-9xl"
              style={{fontSize: "12rem"}}
            >
              403
            </Title>
            <div className="absolute inset-0 flex items-center justify-center">
              <LockOutlined className="text-6xl text-red-500 animate-bounce" />
            </div>
          </div>

          {/* Error Message */}
          <div className="space-y-4">
            <Title level={2} className="!mt-0">
              Access Denied
            </Title>
            <Text className="block max-w-md mx-auto text-gray-500">
              Sorry, but you don't have permission to access this page. Please
              check your credentials or contact the administrator.
            </Text>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col items-center justify-center gap-4 mt-8 sm:flex-row">
            <Button
              onClick={() => navigate(-1)}
              icon={<RollbackOutlined />}
              size="large"
              className="min-w-[160px] flex items-center justify-center gap-2 border-red-200 text-red-500 hover:text-red-600 hover:border-red-300"
            >
              Go Back
            </Button>
            <Button
              onClick={() => navigate("/")}
              type="primary"
              icon={<HomeOutlined />}
              size="large"
              className="min-w-[160px] flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 border-none"
            >
              Home Page
            </Button>
          </div>

          {/* Additional Links */}
          <div className="pt-8 space-y-4">
            <Text className="text-gray-400">Need Help?</Text>
            <div className="flex justify-center gap-6 text-sm">
              <Link
                href="/contact"
                className="flex items-center gap-2 text-red-500 hover:text-red-600"
              >
                <ContactsOutlined /> Contact Support
              </Link>
              <Link
                href="/login"
                className="flex items-center gap-2 text-red-500 hover:text-red-600"
              >
                <LockOutlined /> Login Again
              </Link>
            </div>
          </div>
        </div>

        {/* Bottom Message */}
        <Text className="block mt-12 text-sm text-gray-400">
          If you believe this is a mistake, please contact your system
          administrator.
        </Text>
      </div>

      {/* Animated Border Effect */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute inset-0 border-8 border-red-50 animate-pulse" />
      </div>
    </div>
  );
};

export default UnauthorizedPage;
