"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { useQuery } from "@tanstack/react-query";
import { Loader2, AlertCircle } from "lucide-react";

import { useAppStore } from "@/lib/store";
import { fetchConfig, fetchContext, fetchEvaluateRotations, fetchGibsLayers } from "@/lib/api";

import BrandHeader from "@/components/header/BrandHeader";
import SidebarToggle from "@/components/header/SidebarToggle";
import ViewTabs from "@/components/header/ViewTabs";
import LanguageSwitch from "@/components/header/LanguageSwitch";
import LocationBar from "@/components/field/LocationBar";
import SidebarPanel from "@/components/sidebar/SidebarPanel";

import HeroStatus from "@/components/field/HeroStatus";
import KpiGrid from "@/components/field/KpiGrid";
import WaterBalanceChart from "@/components/charts/WaterBalanceChart";
import TemperatureChart from "@/components/charts/TemperatureChart";
import FrostHeatChart from "@/components/charts/FrostHeatChart";
import CropCalendarTimeline from "@/components/charts/CropCalendarTimeline";
import NdviCurveChart from "@/components/charts/NdviCurveChart";
import SoilSummary from "@/components/field/SoilSummary";
import DataGaps from "@/components/field/DataGaps";

import SummaryBox from "@/components/options/SummaryBox";
import ComparisonTable from "@/components/options/ComparisonTable";
import FitByYearTypeChart from "@/components/charts/FitByYearTypeChart";
import RotationOptionCard from "@/components/options/RotationOptionCard";

import GlossaryView from "@/components/glossary/GlossaryView";

// Dynamically import Leaflet Map to ensure no SSR window errors
const MapContainer = dynamic(() => import("@/components/map/MapContainer"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[340px] bg-[#FAF9F5] rounded-xl border border-[#D5D0C5] flex items-center justify-center text-xs text-[#7B8A7C]">
      Loading satellite map tiles...
    </div>
  ),
});

export default function FieldShiftDashboard() {
  const view = useAppStore((s) => s.view);
  const lat = useAppStore((s) => s.lat);
  const lon = useAppStore((s) => s.lon);
  const currentCrops = useAppStore((s) => s.currentCrops);
  const weights = useAppStore((s) => s.weights);
  const whatIf = useAppStore((s) => s.whatIf);
  const setTranslations = useAppStore((s) => s.setTranslations);

  const sidebarPinned = useAppStore((s) => s.sidebarPinned);
  const setSidebarPinned = useAppStore((s) => s.setSidebarPinned);
  const [hoverSpread, setHoverSpread] = useState(false);

  // Automatic spreading when cursor hits the left edge
  useEffect(() => {
    if (sidebarPinned) {
      setHoverSpread(false);
      return;
    }

    const handleMouseMove = (e: MouseEvent) => {
      // Left edge zone: within 16px of the left edge of the viewport
      if (e.clientX <= 16) {
        setHoverSpread(true);
      }
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, [sidebarPinned]);

  const handleDrawerMouseLeave = (e: React.MouseEvent) => {
    // If cursor moves out to the right (main content area), gracefully retract the spread drawer
    if (e.clientX > 380) {
      setHoverSpread(false);
    }
  };

  // 1. Fetch Config (Crops, Demo Fields, Profiles, Translations, Glossary)
  const { data: config, isLoading: isConfigLoading } = useQuery({
    queryKey: ["config"],
    queryFn: fetchConfig,
  });

  // Sync translations when config loads
  useEffect(() => {
    if (config?.translations) {
      setTranslations(config.translations);
    }
  }, [config, setTranslations]);

  // 2. Fetch Field Context (Climate, KPIs, Soil, Satellite)
  const {
    data: context,
    isLoading: isContextLoading,
    error: contextError,
  } = useQuery({
    queryKey: ["context", lat, lon, whatIf.rainPct, whatIf.tempC],
    queryFn: () => fetchContext(lat, lon, whatIf.rainPct, whatIf.tempC),
  });

  // 3. Fetch Rotations Evaluation (Candidates, Scores, Radar, Explanations)
  const {
    data: evaluation,
    isLoading: isEvalLoading,
    error: evalError,
  } = useQuery({
    queryKey: [
      "evaluation",
      lat,
      lon,
      whatIf.rainPct,
      whatIf.tempC,
      currentCrops,
      whatIf.supply,
      weights,
    ],
    queryFn: () =>
      fetchEvaluateRotations(
        lat,
        lon,
        whatIf.rainPct,
        whatIf.tempC,
        currentCrops,
        whatIf.supply,
        weights
      ),
    enabled: currentCrops.length > 0,
  });

  // 4. Fetch NASA GIBS Layers
  const { data: gibsLayers = [] } = useQuery({
    queryKey: ["gibs-layers"],
    queryFn: fetchGibsLayers,
  });

  return (
    <div className="min-h-screen flex flex-col max-w-[1440px] mx-auto px-4 py-4 sm:px-6 sm:py-6 space-y-4">
      {/* Top Header */}
      <header className="flex flex-wrap items-center justify-between gap-3 pb-2 border-b border-[#E3DFD3]">
        <div className="flex items-center gap-3">
          <BrandHeader />
          <SidebarToggle />
        </div>
        <div className="flex flex-wrap items-center gap-2.5">
          <ViewTabs />
          <LanguageSwitch />
        </div>
      </header>

      {/* Farmland Location Bar */}
      {config && <LocationBar demoFields={config.demo_fields} />}

      {/* Left-edge trigger zone for automatic spreading */}
      {!sidebarPinned && (
        <div
          className="fixed top-0 left-0 bottom-0 w-3 hover:w-6 z-40 cursor-pointer group flex items-center justify-start transition-all"
          onMouseEnter={() => setHoverSpread(true)}
          onClick={() => setHoverSpread(true)}
          title="Move cursor here or click to open controls"
        >
          <div className="h-24 w-1.5 ml-0.5 rounded-r-full bg-[#2F6B45]/40 group-hover:bg-[#2F6B45] group-hover:w-2 transition-all shadow-sm" />
        </div>
      )}

      {/* Flyout Drawer for Hover-Spread Mode (when unpinned) */}
      {!sidebarPinned && (
        <>
          {/* Backdrop overlay */}
          <div
            className={`fixed inset-0 bg-black/25 z-40 backdrop-blur-[1px] transition-opacity duration-300 ${
              hoverSpread ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
            }`}
            onClick={() => setHoverSpread(false)}
          />

          {/* Drawer container */}
          <aside
            onMouseLeave={handleDrawerMouseLeave}
            className={`fixed inset-y-0 left-0 w-[420px] max-w-[92vw] z-50 bg-[#FAF9F5] shadow-2xl border-r border-[#D5D0C5] p-4 sm:p-5 overflow-y-auto transform transition-transform duration-300 ease-out ${
              hoverSpread ? "translate-x-0" : "-translate-x-full"
            }`}
          >
            <SidebarPanel
              config={config}
              mode="drawer"
              onPin={() => {
                setSidebarPinned(true);
                setHoverSpread(false);
              }}
              onClose={() => setHoverSpread(false)}
            />
          </aside>
        </>
      )}

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Left Sidebar: Controls when pinned */}
        {sidebarPinned && (
          <aside className="lg:col-span-4 space-y-4 transition-all duration-300">
            <SidebarPanel
              config={config}
              mode="pinned"
              onCollapse={() => setSidebarPinned(false)}
            />
          </aside>
        )}

        {/* Right Area: Dynamic Views (expands to 12 cols when collapsed) */}
        <main
          className={`${
            sidebarPinned ? "lg:col-span-8" : "lg:col-span-12"
          } space-y-5 transition-all duration-300`}
        >
          {/* Loading or Error states */}
          {(isContextLoading || isEvalLoading || isConfigLoading) && (
            <div className="p-8 rounded-2xl bg-white border border-[#E3DFD3] flex items-center justify-center gap-3 text-sm text-[#2F6B45] font-semibold">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Analyzing NASA climate series & scoring crop rotations...</span>
            </div>
          )}

          {contextError && (
            <div className="p-4 rounded-xl bg-[#FDF0ED] border border-[#F8C8BE] text-xs text-[#C84B31] flex items-start gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{String(contextError)}</span>
            </div>
          )}

          {evalError && (
            <div className="p-4 rounded-xl bg-[#FDF0ED] border border-[#F8C8BE] text-xs text-[#C84B31] flex items-start gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{String(evalError)}</span>
            </div>
          )}

          {/* VIEW 1: YOUR FIELD */}
          {view === "field" && context && evaluation && (
            <div className="space-y-4">
              <HeroStatus context={context} />
              <MapContainer layers={gibsLayers} />
              <KpiGrid kpis={context.kpis} />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <WaterBalanceChart data={context.monthly_climatology} />
                <TemperatureChart data={context.monthly_climatology} />
              </div>

              <FrostHeatChart
                frost={context.frost_probability}
                heat={context.heat_days}
              />

              <CropCalendarTimeline
                plantings={evaluation.options[0]?.plantings || []}
                bareDays={evaluation.options[0]?.bare_days_per_year || 0}
              />

              <NdviCurveChart satellite={context.satellite} />
              <SoilSummary soil={context.soil} satellite={context.satellite} />
              <DataGaps gaps={context.gaps} />
            </div>
          )}

          {/* VIEW 2: ROTATION OPTIONS */}
          {view === "options" && evaluation && (
            <div className="space-y-4">
              <SummaryBox summaryBox={evaluation.summary_box} />
              <ComparisonTable
                options={evaluation.options}
                bestFitIndex={evaluation.best_fit_index}
              />
              <FitByYearTypeChart options={evaluation.options} />

              <div className="space-y-2 pt-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324]">
                  Detailed Candidate Evaluations
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {evaluation.options.map((opt, i) => (
                    <RotationOptionCard
                      key={opt.index}
                      option={opt}
                      currentOption={evaluation.options[0]}
                      colorIndex={i}
                    />
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* VIEW 3: GLOSSARY & SOURCES */}
          {view === "glossary" && config && (
            <GlossaryView glossary={config.glossary} />
          )}
        </main>
      </div>

      {/* Footer */}
      <footer className="pt-6 pb-4 border-t border-[#EAE6DC] text-center text-xs text-[#7B8A7C]">
        <p>
          Field Shift · NASA Space Apps Challenge 2026 · Powered by NASA POWER, ISRIC SoilGrids, MODIS Terra NDVI & SMAP Radiometry.
        </p>
      </footer>
    </div>
  );
}
