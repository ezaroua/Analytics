import {
  ArrowLeftOutlined,
  HomeOutlined,
  MehOutlined,
  QuestionCircleOutlined,
} from "@ant-design/icons";
import {Button} from "antd";
import {useNavigate} from "react-router-dom";
import "./NotFoundPage.css";

const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="w-full max-w-2xl space-y-8 text-center">
        {/* 👇 Animated 404 Number 👇 */}
        <div className="relative">
          <h1 className="font-bold text-gray-200 text-9xl animate-pulse">
            404
          </h1>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="space-y-4 text-gray-800">
              <h2 className="text-2xl font-semibold">Oops! Page not found</h2>
              <p className="max-w-md mx-auto text-gray-600">
                The page you're looking for doesn't exist or has been moved.
              </p>
            </div>
          </div>
        </div>

        {/* 👇 Illustration 👇 */}
        <div className="relative w-48 h-48 mx-auto">
          <div className="absolute inset-0 animate-float">
            <MehOutlined className="text-blue-500 text-8xl" />
          </div>
        </div>

        {/* 👇 Action Buttons 👇 */}
        <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Button
            onClick={() => navigate(-1)}
            icon={<ArrowLeftOutlined />}
            size="large"
            className="min-w-[160px] flex items-center justify-center"
          >
            Go Back
          </Button>
          <Button
            onClick={() => navigate("/")}
            type="primary"
            icon={<HomeOutlined />}
            size="large"
            className="min-w-[160px] flex items-center justify-center bg-blue-500 hover:bg-blue-600"
          >
            Home Page
          </Button>
        </div>

        {/* 👇 Help Text 👇 */}
        <p className="flex items-center justify-center gap-2 mt-8 text-sm text-gray-500">
          <QuestionCircleOutlined /> Need assistance?
          <a href="/contact" className="text-blue-500 hover:underline">
            Contact Support
          </a>
        </p>
      </div>
    </div>
  );
};

export default NotFoundPage;
