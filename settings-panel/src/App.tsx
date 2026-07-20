import AppLayout from "@/Pages/__LAYOUT/AppLayout";
import ErrorPage from "@/Pages/__LAYOUT/ErrorPage";

import { RouterProvider  } from "react-router/dom";
import { createBrowserRouter } from "react-router";
import "./App.css";

const browserRouter = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
  },
  {
    path: "*",
    element: <ErrorPage />,
  }
])

function App() {

  return <RouterProvider router={browserRouter} />;
}

export default App;