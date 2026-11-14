"use client";

import React, { useState } from "react";
import { AlertCircle, ChevronDown, ChevronUp } from "lucide-react";
import { useTranslation } from "@/lib/i18n";

interface DataGapsProps {
  gaps: { en: string; uz: string }[];
}

export default function DataGaps({ gaps }: DataGapsProps) {
  const { t, language } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);

  if (!gaps || gaps.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] shadow-xs overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between text-left hover:bg-[#FAF9F5] transition-colors cursor-pointer"
      >
        <div className="flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-[#D97706]" />
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324]">
            {t("f.gaps") || "Data Caveats & Information Gaps"} ({gaps.length})
          </h4>
        </div>
        {isOpen ? (
          <ChevronUp className="w-4 h-4 text-[#7B8A7C]" />
        ) : (
          <ChevronDown className="w-4 h-4 text-[#7B8A7C]" />
        )}
      </button>

      {isOpen && (
        <div className="p-4 pt-0">
          <ul className="space-y-1.5 text-xs text-[#526356]">
            {gaps.map((g, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-[#D97706] font-bold">•</span>
                <span>{language === "uz" ? g.uz : g.en}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
