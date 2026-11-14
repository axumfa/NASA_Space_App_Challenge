import { create } from "zustand";

export interface AppState {
  language: "en" | "uz";
  view: "field" | "options" | "glossary";
  fieldChoice: string;
  fieldName: string;
  lat: number;
  lon: number;
  currentCrops: string[];
  profile: string;
  weights: Record<string, number>;
  whatIf: {
    rainPct: number;
    tempC: number;
    supply: number; // 0.4 to 1.0
  };
  translations: Record<string, { en: string; uz?: string }>;
  sidebarPinned: boolean;

  // Actions
  setLanguage: (lang: "en" | "uz") => void;
  setView: (view: "field" | "options" | "glossary") => void;
  setSidebarPinned: (pinned: boolean | ((prev: boolean) => boolean)) => void;
  selectField: (
    key: string,
    name: string,
    lat: number,
    lon: number,
    defaultRotation?: string[]
  ) => void;
  setCoordinates: (lat: number, lon: number) => void;
  setCrop: (index: number, cropId: string) => void;
  setProfile: (profileName: string, profileWeights?: Record<string, number>) => void;
  setWeight: (key: string, value: number) => void;
  setWhatIf: (rainPct: number, tempC: number, supply: number) => void;
  setTranslations: (dict: Record<string, { en: string; uz?: string }>) => void;
}

export const useAppStore = create<AppState>((set) => ({
  language: "en",
  view: "field",
  fieldChoice: "fergana",
  fieldName: "Fergana Valley, Uzbekistan",
  lat: 40.4229,
  lon: 71.7576,
  currentCrops: ["winter_wheat", "cotton"],
  profile: "Balanced",
  weights: {
    water_saving: 5,
    soil_om: 5,
    nitrogen: 5,
    erosion: 5,
    forage: 5,
    income: 5,
  },
  whatIf: {
    rainPct: 0,
    tempC: 0.0,
    supply: 1.0,
  },
  translations: {},
  sidebarPinned: true,

  setLanguage: (lang) => set({ language: lang }),
  setView: (view) => set({ view }),
  setSidebarPinned: (pinned) =>
    set((state) => ({
      sidebarPinned:
        typeof pinned === "function" ? pinned(state.sidebarPinned) : pinned,
    })),
  selectField: (key, name, lat, lon, defaultRotation) =>
    set((state) => ({
      fieldChoice: key,
      fieldName: name,
      lat,
      lon,
      currentCrops: defaultRotation && defaultRotation.length > 0 ? defaultRotation : state.currentCrops,
    })),
  setCoordinates: (lat, lon) =>
    set({
      lat,
      lon,
      fieldChoice: "own",
      fieldName: "My own location",
    }),
  setCrop: (index, cropId) =>
    set((state) => {
      const crops = [...state.currentCrops];
      if (cropId === "—" || !cropId) {
        crops.splice(index, 1);
      } else {
        crops[index] = cropId;
      }
      return { currentCrops: crops };
    }),
  setProfile: (profileName, profileWeights) =>
    set((state) => ({
      profile: profileName,
      weights: profileWeights ? { ...profileWeights } : state.weights,
    })),
  setWeight: (key, value) =>
    set((state) => ({
      weights: { ...state.weights, [key]: value },
    })),
  setWhatIf: (rainPct, tempC, supply) =>
    set({
      whatIf: { rainPct, tempC, supply },
    }),
  setTranslations: (translations) => set({ translations }),
}));
