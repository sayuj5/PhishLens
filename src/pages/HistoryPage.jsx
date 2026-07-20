import { motion } from "framer-motion";
import { Archive, ShieldAlert, ShieldCheck, Shield } from "lucide-react";

const mockHistory = [
  {
    id: 1,
    url: "https://secure-update-login.account.xyz/auth",
    score: 85,
    date: "2026-07-20 14:32",
  },
  {
    id: 2,
    url: "http://192.168.1.104/payload.exe",
    score: 95,
    date: "2026-07-20 12:15",
  },
  {
    id: 3,
    url: "https://github.com/phishlens",
    score: 10,
    date: "2026-07-19 09:45",
  },
  {
    id: 4,
    url: "https://paypal-security-check.com",
    score: 65,
    date: "2026-07-18 16:20",
  },
];

export default function HistoryPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex-1 py-8 flex flex-col"
    >
      <div className="flex items-center gap-4 mb-10">
        <Archive className="w-8 h-8 text-accent" />
        <div>
          <h1 className="text-2xl font-display font-bold tracking-widest uppercase">
            Analysis Archive
          </h1>
          <p className="text-xs text-textSecondary uppercase tracking-widest mt-1">
            Local session history
          </p>
        </div>
      </div>

      <div className="glass-panel overflow-hidden">
        <div className="grid grid-cols-12 gap-4 p-4 border-b border-white/5 bg-white/5 text-[10px] font-bold tracking-widest text-textSecondary uppercase">
          <div className="col-span-6 md:col-span-8">Target URL</div>
          <div className="col-span-3 md:col-span-2 text-center">Score</div>
          <div className="col-span-3 md:col-span-2 text-right">Date</div>
        </div>

        <div className="flex flex-col">
          {mockHistory.map((item, idx) => (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              key={item.id}
              className="grid grid-cols-12 gap-4 p-4 border-b border-white/5 hover:bg-white/5 transition-colors items-center"
            >
              <div className="col-span-6 md:col-span-8 font-mono text-xs text-white/90 truncate pr-4">
                {item.url}
              </div>
              <div className="col-span-3 md:col-span-2 flex justify-center">
                <div
                  className={`flex items-center gap-2 px-3 py-1 rounded text-xs font-bold ${
                    item.score >= 75
                      ? "bg-danger/20 text-danger"
                      : item.score >= 40
                        ? "bg-warning/20 text-warning"
                        : "bg-success/20 text-success"
                  }`}
                >
                  {item.score >= 75 ? (
                    <ShieldAlert className="w-3 h-3" />
                  ) : item.score >= 40 ? (
                    <Shield className="w-3 h-3" />
                  ) : (
                    <ShieldCheck className="w-3 h-3" />
                  )}
                  {item.score}
                </div>
              </div>
              <div className="col-span-3 md:col-span-2 text-right text-xs text-textSecondary font-mono">
                {item.date}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
