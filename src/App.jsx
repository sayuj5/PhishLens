import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import { Navbar } from "./components/Navbar";
import ScannerPage from "./pages/ScannerPage";
import ReportPage from "./pages/ReportPage";
import HistoryPage from "./pages/HistoryPage";
import ApiPage from "./pages/ApiPage";
import { AnimatePresence } from "framer-motion";

function AnimatedRoutes() {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<ScannerPage />} />
        <Route path="/report" element={<ReportPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/api" element={<ApiPage />} />
        <Route path="*" element={<ScannerPage />} />
      </Routes>
    </AnimatePresence>
  );
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background text-textPrimary relative overflow-x-hidden font-sans">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[70vw] h-[70vw] rounded-full bg-glow/5 blur-[150px] pointer-events-none z-0"></div>
        <Navbar />
        <main className="relative z-10 pt-24 min-h-screen flex flex-col px-4 md:px-12 lg:px-24 pb-16">
          <AnimatedRoutes />
        </main>
      </div>
    </Router>
  );
}
