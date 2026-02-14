import { BrowserRouter } from "react-router-dom"
import { ConfigProvider } from "antd"
import { AppRoutes } from "./Routes"
import AuthProvider from "./context/AuthContext"
import { ErrorBoundary } from "react-error-boundary"

import SmartFallback from "./pages/Errors/SmartFallback"

export default function App() {

  return (
    <BrowserRouter>
        <AuthProvider>
          <ErrorBoundary
            FallbackComponent={SmartFallback}
          >
            <ConfigProvider 
              theme={{
                token: {
                  fontSize: 16,
                },
                components: {
                  Breadcrumb: {
                    lastItemColor: '#FFF',
                    separatorColor: 'rgba(255 255 255 / 0.6)',
                    linkColor: 'rgba(255 255 255 / 0.6)',
                    linkHoverColor: '#FFF',
                    fontSize: 14,
                  }
                }
              }}
            >
              <AppRoutes />
            </ConfigProvider>
          </ErrorBoundary>
        </AuthProvider>
    </BrowserRouter>
  )
}
