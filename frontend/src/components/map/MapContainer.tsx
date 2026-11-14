"use client";

import React, { useEffect, useState, useRef } from "react";
import L from "leaflet";
import { Layers, MapPin } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { useTranslation } from "@/lib/i18n";
import type { GibsLayerItem } from "@/types";

interface MapContainerProps {
  layers: GibsLayerItem[];
}

export default function MapContainer({ layers }: MapContainerProps) {
  const { t } = useTranslation();
  const mapRef = useRef<HTMLDivElement>(null);
  const leafletMap = useRef<L.Map | null>(null);
  const markerRef = useRef<L.Marker | null>(null);
  const gibsLayerRef = useRef<L.TileLayer | null>(null);

  const lat = useAppStore((s) => s.lat);
  const lon = useAppStore((s) => s.lon);
  const setCoordinates = useAppStore((s) => s.setCoordinates);

  const [activeLayerKey, setActiveLayerKey] = useState<string>("none");

  // Fix default marker icon issue in Leaflet with webpack/bundlers
  useEffect(() => {
    delete (L.Icon.Default.prototype as any)._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
      iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
      shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    });
  }, []);

  // Initialize Map
  useEffect(() => {
    if (!mapRef.current || leafletMap.current) return;

    const map = L.map(mapRef.current, {
      center: [lat, lon],
      zoom: 10,
      zoomControl: true,
    });

    // High quality satellite imagery basemap
    const esriSatellite = L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      {
        attribution: "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
        maxZoom: 18,
      }
    ).addTo(map);

    // Marker
    const marker = L.marker([lat, lon]).addTo(map);
    markerRef.current = marker;

    // Click handler to re-center
    map.on("click", (e: L.LeafletMouseEvent) => {
      const newLat = parseFloat(e.latlng.lat.toFixed(4));
      const newLon = parseFloat(e.latlng.lng.toFixed(4));
      setCoordinates(newLat, newLon);
    });

    leafletMap.current = map;

    return () => {
      map.remove();
      leafletMap.current = null;
    };
  }, []);

  // Sync center & marker when lat/lon change
  useEffect(() => {
    if (!leafletMap.current || !markerRef.current) return;
    leafletMap.current.setView([lat, lon], leafletMap.current.getZoom());
    markerRef.current.setLatLng([lat, lon]);
  }, [lat, lon]);

  // Handle GIBS Tile Layer Switching
  useEffect(() => {
    if (!leafletMap.current) return;

    if (gibsLayerRef.current) {
      leafletMap.current.removeLayer(gibsLayerRef.current);
      gibsLayerRef.current = null;
    }

    if (activeLayerKey !== "none") {
      const activeLayer = layers.find((l) => l.key === activeLayerKey);
      if (activeLayer && activeLayer.tile_template) {
        // Replace {z}/{y}/{x} in URL
        const tileLayer = L.tileLayer(activeLayer.tile_template, {
          maxZoom: activeLayer.max_zoom || 9,
          opacity: 0.75,
          attribution: "NASA GIBS / EOSDIS",
        }).addTo(leafletMap.current);

        gibsLayerRef.current = tileLayer;
      }
    }
  }, [activeLayerKey, layers]);

  const activeLayerObj = layers.find((l) => l.key === activeLayerKey);

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-[#1A3324]">
          <MapPin className="w-3.5 h-3.5 text-[#2F6B45]" />
          <span>Interactive Farmland & NASA GIBS Viewer</span>
        </div>

        {/* GIBS Layer Switcher */}
        <div className="flex items-center gap-1.5 bg-[#FAF9F5] p-1 rounded-xl border border-[#E0DCD3]">
          <Layers className="w-3.5 h-3.5 text-[#526356] ml-1.5" />
          <select
            value={activeLayerKey}
            onChange={(e) => setActiveLayerKey(e.target.value)}
            className="text-xs bg-transparent border-none text-[#1A3324] font-semibold focus:outline-none cursor-pointer pr-2"
          >
            <option value="none">Base Satellite Imagery</option>
            {layers.map((l) => (
              <option key={l.key} value={l.key} disabled={!l.ok}>
                {l.key === "ndvi"
                  ? "MODIS NDVI Vegetation (8-Day)"
                  : l.key === "precip"
                  ? "IMERG Precipitation Rate"
                  : l.key === "temp"
                  ? "Land Surface Temperature"
                  : "SMAP Soil Moisture"}
                {!l.ok ? " (Unavailable)" : ""}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Map Container */}
      <div className="relative w-full h-[340px] rounded-xl overflow-hidden border border-[#D5D0C5] z-0">
        <div ref={mapRef} className="w-full h-full" />

        {/* Dynamic Colormap Legend Overlay */}
        {activeLayerObj && activeLayerObj.ok && activeLayerObj.css_gradient !== "none" && (
          <div className="absolute bottom-3 left-3 bg-white/95 backdrop-blur-xs p-2.5 rounded-xl border border-[#D5D0C5] shadow-md z-[1000] w-56 text-[11px]">
            <div className="font-bold text-[#1A3324] mb-1 flex justify-between">
              <span>{activeLayerObj.key.toUpperCase()} Layer</span>
              <span className="text-[#68786A]">{activeLayerObj.date}</span>
            </div>
            <div
              className="h-2.5 rounded-full border border-black/10 my-1"
              style={{ background: activeLayerObj.css_gradient }}
            />
            <div className="flex justify-between text-[10px] font-mono text-[#526356]">
              <span>{activeLayerObj.vmin ?? 0}</span>
              <span>{activeLayerObj.unit}</span>
              <span>{activeLayerObj.vmax ?? 1}</span>
            </div>
          </div>
        )}
      </div>

      <div className="flex items-center justify-between text-[11px] text-[#7B8A7C]">
        <span>Click anywhere on the map to re-center and analyze custom coordinates.</span>
        <span className="font-mono">Lat: {lat.toFixed(4)}, Lon: {lon.toFixed(4)}</span>
      </div>
    </div>
  );
}
