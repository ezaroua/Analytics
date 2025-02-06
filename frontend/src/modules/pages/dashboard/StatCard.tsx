import {Card, Statistic} from "antd";
import {ArrowUpOutlined, ArrowDownOutlined} from "@ant-design/icons";

interface StatsCardProps {
  title: string;
  value: number;
  prefix?: React.ReactNode;
  suffix?: string;
  trend?: number;
  loading?: boolean;
}

export const StatsCard = ({
  title,
  value,
  prefix,
  suffix,
  trend,
  loading,
}: StatsCardProps) => {
  return (
    <Card loading={loading} bordered={false} className="h-full">
      <Statistic
        title={<span className="text-gray-600 font-medium">{title}</span>}
        value={value}
        prefix={prefix}
        suffix={suffix}
        valueStyle={{color: "#1677ff"}}
      />
      {trend !== undefined && (
        <div
          className={`mt-2 flex items-center ${
            trend >= 0 ? "text-green-500" : "text-red-500"
          }`}
        >
          {trend >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
          <span className="ml-1">{Math.abs(trend)}%</span>
        </div>
      )}
    </Card>
  );
};
