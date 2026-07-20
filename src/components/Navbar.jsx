import { Link, useLocation } from "react-router-dom";
import { ShieldAlert, Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";

const navItems = [
  { path: "/", label: "ANALYZE" },
  { path: "/history", label: "ARCHIVE" },
  { path: "/api", label: "SENSORS" },
];

export function Navbar() {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      <nav className="glass-nav fixed top-0 w-full z-50 flex items-center justify-between px-6 md:px-12 py-4">
        <Link to="/" className="flex items-center gap-3 group">
          <img
            src="/phishlens_logo.png"
            alt="PhishLens Logo"
            className="w-8 h-8 object-contain group-hover:scale-110 transition-transform duration-500"
          />
          <span className="text-lg font-display font-bold tracking-[0.2em] text-textPrimary">
            PHISHLENS
          </span>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex gap-10 text-xs font-semibold text-textSecondary uppercase tracking-[0.2em]">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`relative pb-2 transition-colors ${isActive ? "text-white" : "hover:text-white"}`}
              >
                {item.label}
                {isActive && (
                  <motion.div
                    layoutId="navbar-indicator"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
              </Link>
            );
          })}
        </div>

        <div className="hidden md:block">
          <a
            href="mailto:enterprise@phishlens.com"
            className="relative overflow-hidden group bg-accent text-[#0d0c0c] px-6 py-2.5 rounded-sm uppercase text-xs font-bold tracking-widest transition-all hover:shadow-[0_0_20px_rgba(230,115,54,0.4)] block"
          >
            <span className="relative z-10">Enquire</span>
            <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
          </a>
        </div>

        {/* Mobile Toggle */}
        <button
          className="md:hidden text-textPrimary p-2"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? (
            <X className="w-6 h-6" />
          ) : (
            <Menu className="w-6 h-6" />
          )}
        </button>
      </nav>

      {/* Mobile Nav */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-0 z-40 bg-background/95 backdrop-blur-xl pt-24 px-6 flex flex-col gap-8 md:hidden"
          >
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`text-xl font-display font-bold tracking-widest uppercase ${location.pathname === item.path ? "text-accent" : "text-textPrimary"}`}
              >
                {item.label}
              </Link>
            ))}
            <a
              href="mailto:enterprise@phishlens.com"
              className="bg-accent text-[#0d0c0c] px-6 py-4 rounded-sm uppercase text-sm font-bold tracking-widest mt-auto mb-12 w-full text-center block"
            >
              Enquire
            </a>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
