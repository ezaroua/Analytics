import { createBrowserRouter } from "react-router-dom";
import { AnalysisPage } from "../../modules/pages/analysis/AnalysisPage";
import { Dashboard } from "../../modules/pages/dashboard/Dashboard";
import { DashboardLayout } from "../../modules/pages/dashboard/DashboardLayout";
import FileHistoryPage from "../../modules/pages/fileHistory/FileHistory";
import { FileUploadPage } from "../../modules/pages/fileUpload/FileUploadPage";

import { NotificationSettingsPage } from "../../modules/pages/notifications/NotificationSettingsPage";
import NotFoundPage from "../pages/NotFoundPage";
import UnauthorizedPage from "../pages/UnauthorizedPage";

export const ROUTE_PATH = {
  // ! Main public routes
  public: {
    HOME: "/",
    DASHBOARD: "/dashboard",
    FILE_UPLOAD: "/upload",
    ANALYSIS: "/analysis/:fileId", // Dynamic route for specific file analysis
    HISTORY: "/history",
    NOTIFICATIONS: "/notifications",
  },

  // ! Error routes
  error: {
    UNAUTHORIZED: "/unauthorized",
    NOT_FOUND: "*",
  },
} as const;

// * Type for extracting route path types

export const appRoutes = [
  {
    path: ROUTE_PATH.public.HOME,
    element: <DashboardLayout />,
    children: [
      {
        path: ROUTE_PATH.public.HOME,
        element: <Dashboard />,
      },
      {
        path: ROUTE_PATH.public.DASHBOARD,
        element: <Dashboard />,
      },
      {
        path: ROUTE_PATH.public.FILE_UPLOAD,
        element: <FileUploadPage />,
      },
      {
        path: ROUTE_PATH.public.ANALYSIS,
        element: <AnalysisPage />,
      },
      {
        path: ROUTE_PATH.public.HISTORY,
        element: <FileHistoryPage />,
      },
      {
        path: ROUTE_PATH.public.NOTIFICATIONS,
        element: <NotificationSettingsPage />,
      },
    ],
  },
  {
    path: ROUTE_PATH.error.UNAUTHORIZED,
    element: <UnauthorizedPage />,
  },
  {
    path: ROUTE_PATH.error.NOT_FOUND,
    element: <NotFoundPage />,
  },
];

export const router = createBrowserRouter(appRoutes);
