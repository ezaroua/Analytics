import {Breadcrumb} from "antd";
import {Link } from "react-router-dom";
import { ROUTE_PATH } from "../../shared/routes";

export const PageHeader = () => {
  // const location = useLocation();
  // const pathElements = location.pathname.split("/").filter(Boolean);

  const getBreadcrumbItems = () => {
    const items = [
      {
        title : <Link to={ROUTE_PATH.public.DASHBOARD}>Dashboard</Link>,
      },
    ];

    // pathElements.forEach((path, index) => {
    //   // const url = `/${pathElements.slice(0, index + 1).join("/")}`;
    //   // items.push({
    //   //   title: path.charAt(0).toUpperCase() + path.slice(1),
    //   //   href: url,
    //   // });
    // });

    return items;
  };

  return <Breadcrumb items={getBreadcrumbItems()} />;
};
