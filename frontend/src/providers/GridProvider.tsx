import { createContext, useContext, useEffect, useRef, useState } from "react";
import { getRandomGrid, clearGrid, nextStep } from "../api/grid";

type Grid = number[][]

type GridContextType = {
  grid: Grid;
  isPlaying: boolean;
  randomize: () => void;
  clear: () => void;
  stepForward: () => void;
  play: () => void;
  pause: () => void;
};

const GridContext = createContext<GridContextType | null>(null);

export const useGrid = () => {
  const ctx = useContext(GridContext);
  if (!ctx) throw new Error("useGrid must be used within GridProvider");
  return ctx;
};

export const GridProvider = ({ children }: { children: React.ReactNode }) => {
  const [grid, setGrid] = useState<Grid>([]);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  const fetchRandom = async () => {
    const res = await getRandomGrid();
    setGrid(res.data);
    setStep(0);
  };

  const fetchClear = async () => {
    const res = await clearGrid();
    setGrid(res.data);
  };

  const fetchNext = async () => {
    const res = await nextStep();
    setGrid(res.data);
  };

  const startPlaying = () => {
    return undefined
  };

  const stopPlaying = () => {
    return undefined
  };

    //This useEffect ensure that on exit of the provider (usually on refresh) the auto next-step is canceled
  useEffect(() => {
    return stopPlaying; // Cleanup on unmount
  }, []);

  return (
    <GridContext.Provider
      value={{
        grid,
        step,
        isPlaying,
        randomize: fetchRandom,
        clear: fetchClear,
        stepForward: fetchNext,
        play: startPlaying,
        pause: stopPlaying,
      }}
    >
      {children}
    </GridContext.Provider>
  );
};
