import {Card, Tabs} from "antd";
import {Pie} from "@ant-design/plots";
import LineChart from "@ant-design/plots/es/components/line";

export const AnomaliesSummary = () => {
  const data = [
    {type: "Price", value: 23},
    {type: "Quantity", value: 15},
    {type: "Rating", value: 8},
  ];

  return (
    <Card title="Anomalies Summary" className="h-full">
      <Tabs
        items={[
          {
            key: "distribution",
            label: "Distribution",
            children: (
              <div className="h-64">
                <Pie
                  data={data}
                  angleField="value"
                  colorField="type"
                  radius={0.8}
                  label={{type: "outer"}}
                />
              </div>
            ),
          },
          {
            key: "trend",
            label: "Trend",
            children: <LineChart data={[]} />,
          },
        ]}
      />
    </Card>
  );
};
