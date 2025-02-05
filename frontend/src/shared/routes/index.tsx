import {createBrowserRouter} from "react-router-dom";
import App from "../../App";
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
    element: <App />,
    // children: [
    //   {
    //     path: ROUTE_PATH.public.DASHBOARD,
    //     element: <Dashboard />,
    //   },
    //   {
    //     path: ROUTE_PATH.public.FILE_UPLOAD,
    //     element: <FileUpload />,
    //   },
    //   {
    //     path: ROUTE_PATH.public.ANALYSIS,
    //     element: <AnalysisResults />,
    //   },
    //   {
    //     path: ROUTE_PATH.public.HISTORY,
    //     element: <FileHistory />,
    //   },
    //   {
    //     path: ROUTE_PATH.public.NOTIFICATIONS,
    //     element: <NotificationSettings />,
    //   },
    // ],
  },
  // Error routes
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
