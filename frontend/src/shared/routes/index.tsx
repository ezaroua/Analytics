import {createBrowserRouter} from "react-router-dom";
import App from "../../App";

export const ROUTE_PATH = {
  // ! Main public routes
  public: {
    HOME: "/",
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
  },
];

export const router = createBrowserRouter(appRoutes);
