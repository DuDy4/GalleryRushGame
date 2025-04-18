import { createContext, useContext, useEffect, useRef, useState } from "react"
import axios from "axios"

const GRID_SIZE = 20
const API_BASE = "http://localhost:8000/api" // <-- Replace with your actual backend

type GridContextType = {
  grid: boolean[][]
  stepCount: number
  isPlaying: boolean
  speed: number
  setSpeed: (s: number) => void
  randomize: () => void
  clear: () => void
  step: () => void
  togglePlay: () => void
  toggleCell: (i: number, j: number) => void
}

const GridContext = createContext<GridContextType | null>(null)

export const useGrid = () => {
  const ctx = useContext(GridContext)
  if (!ctx) throw new Error("useGrid must be used within GridProvider")
  return ctx
}

export const GridProvider = ({ children }: { children: React.ReactNode }) => {
  const [grid, setGrid] = useState<boolean[][]>([])
  const [stepCount, setStepCount] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [speed, setSpeed] = useState(1)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  const fetchGrid = async (endpoint: string) => {
    try {
      const res = await axios.post(`${API_BASE}${endpoint}`)
      setGrid(res.data.grid)
    } catch (err) {
      console.error(`Failed to fetch ${endpoint}`, err)
    }
  }

  const randomize = () => {
    fetchGrid("/randomize")
    setStepCount(0)
  }

  const clear = () => {
    fetchGrid("/clear")
    setStepCount(0)
  }

  const step = () => {
    fetchGrid("/next")
    setStepCount((prev) => prev + 1)
  }

  const togglePlay = () => {
    setIsPlaying((prev) => !prev)
  }

  const toggleCell = (i: number, j: number) => {
    setGrid((g) => {
      const newGrid = g.map((row) => [...row])
      newGrid[i][j] = !newGrid[i][j]
      return newGrid
    })
  }

  useEffect(() => {
    randomize()
  }, [])

  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        step()
      }, speed * 1000)
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [isPlaying, speed])

  return (
    <GridContext.Provider
      value={{
        grid,
        stepCount,
        isPlaying,
        speed,
        setSpeed,
        randomize,
        clear,
        step,
        togglePlay,
        toggleCell,
      }}
    >
      {children}
    </GridContext.Provider>
  )
}
