import { createContext, useContext, useEffect, useRef, useState } from "react"
import axios from "axios"

const API_BASE: string = import.meta.env.VITE_API_URL || "http://localhost:8000/api"

type GridContextType = {
  grid: boolean[][]
  stepCount: number
  isPlaying: boolean
  isWrapped: boolean
  isTimeTraveling: boolean
  speed: number
  winReason: string
  removeWinReason: () => void
  setSpeed: (s: number) => void
  randomize: () => void
  clear: () => void
  step: () => void
  stepBack: () => void
  togglePlay: () => void
  toggleWrap: () => void
  toggleCell: (i: number, j: number) => void
  toggleTimeTraveling: () => void
}

const GridContext = createContext<GridContextType | null>(null)

export const useGrid = () => {
  const ctx = useContext(GridContext)
  if (!ctx) throw new Error("useGrid must be used within GridProvider")
  return ctx
}

export const GridProvider = ({ children }: { children: React.ReactNode }) => {
  //This is the heavy lifter provider. All connection to the backend will be done from here.

  const [grid, setGrid] = useState<boolean[][]>([])
  const [stepCount, setStepCount] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isWrapped, setIsWrapped] = useState(false)
  const [isTimeTraveling, setIsTimeTraveling] = useState(false)
  const [speed, setSpeed] = useState(1)
  const [winReason, setWinReason] = useState("")
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const fetchGrid = async (endpoint: string) => {
    try {
      const res = await axios.post(`${API_BASE}${endpoint}`)
      const data = res.data
      if (!data) return null
      if (data.win_reason){
        console.log(data.win_reason)
        setWinReason(data.win_reason)
        setIsPlaying(false)
      }
      setGrid(data.grid)
      setStepCount(data.steps)
      setIsWrapped(data.wrap)
    } catch (err) {
      console.error(`Failed to fetch ${endpoint}`, err)
    }
  }

  const randomize = () => {
    fetchGrid("/randomize")
  }

  const clear = () => {
    fetchGrid("/clear")
  }

  const step = () => {
    fetchGrid("/next")
  }

  const wrap = async () => {
    await fetchGrid("/wrap")
  }

  const stepBack = () => {
    fetchGrid("/previous")
  }

  const removeWinReason = () => {
    setWinReason("")
  }

  //This is the request for the current grid
  const touch = async () => {
    try {
      const res = await axios.get(`${API_BASE}/`)
      setGrid(res.data.grid)
      setStepCount(res.data.steps)
    } catch (err) {
      console.error(`Failed to fetch current `, err)
    }
  }

  const togglePlay = () => {
    setIsPlaying((prev) => !prev)
  }

  const toggleWrap = async () => {
    await wrap()
  }

  const toggleTimeTraveling = () => {
    setIsTimeTraveling((prev) => !prev)
  }

  const update = async (i: number, j: number) => {
    try {
      await axios.put(`${API_BASE}/update`, {"position": [i, j] })
    } catch (err) {
      console.error(`Failed to update edition`, err)
    }
  }

  const toggleCell = (i: number, j: number) => {
    setGrid((g) => {
      const newGrid = g.map((row) => [...row])
      newGrid[i][j] = !newGrid[i][j]
      update(i, j)
      return newGrid
    })
  }

  useEffect(() => {
    touch()
  }, [])

  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        isTimeTraveling ? stepBack() : step()
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
  }, [isPlaying, isTimeTraveling, speed])

  return (
    <GridContext.Provider
      value={{
        grid,
        stepCount,
        isPlaying,
        isWrapped,
        isTimeTraveling,
        speed,
        winReason,
        removeWinReason,
        setSpeed,
        randomize,
        clear,
        step,
        stepBack,
        togglePlay,
        toggleCell,
        toggleWrap,
        toggleTimeTraveling,
      }}
    >
      {children}
    </GridContext.Provider>
  )
}
