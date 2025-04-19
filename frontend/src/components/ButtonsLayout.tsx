import { Button, Slider, Stack, Typography } from "@mui/material"
import { PlayArrow, Pause, Refresh, Replay, Close } from "@mui/icons-material"
import { useGrid } from "../providers/GridProvider"
import { useEffect } from "react";

export default function ButtonsLayout() {
  const {
    isPlaying,
    speed,
    setSpeed,
    stepCount,
    grid,
    randomize,
    clear,
    step,
    togglePlay,
  } = useGrid()

  //This useEffect start listening to keyboard for the keys we defined -
  // and on return (when closing the component) remove the listener
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (document.activeElement?.tagName === "INPUT") return

      switch (e.key.toLowerCase()) {
        case "r": randomize(); break
        case "c": clear(); break
        case "s": step(); break
        case "p": togglePlay(); break
      }
    }

    window.addEventListener("keydown", handleKey)
    return () => window.removeEventListener("keydown", handleKey)
  }, [randomize, clear, step, togglePlay])

  return (
    <Stack spacing={3} alignItems="center" width="100%">
      <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap">
        <Button onClick={randomize} variant="outlined" startIcon={<Refresh />}>Randomize (R)</Button>
        <Button
          onClick={clear}
          variant="outlined"
          startIcon={<Close />}
        >
          Clear (C)
        </Button>
        <Button
          onClick={step}
          variant="outlined"
          startIcon={<Replay />}
        >
          Step (S)
        </Button>
        <Button
          onClick={togglePlay}
          variant={isPlaying ? "contained" : "outlined"}
          color={isPlaying ? "error" : "primary"}
          startIcon={isPlaying ? <Pause /> : <PlayArrow />}
        >
          {isPlaying ? "Pause" : "Play"} (p)
        </Button>
      </Stack>

      {/* Speed + info */}
      <Stack direction="row" spacing={3} alignItems="center" justifyContent="center" flexWrap="wrap">
        <Typography variant="body2">Speed:</Typography>
        <Slider
          value={speed}
          min={0.1}
          max={2}
          step={0.1}
          onChange={(_, value) => setSpeed(value as number)}
          style={{ width: 200 }}
        />
        <Typography variant="body2">{speed.toFixed(1)}s</Typography>
        <Typography variant="body2">
          Generation: <b>{stepCount}</b>
        </Typography>
        <Typography variant="body2">
          Active Galleries: <b>{grid && grid.flat().filter(Boolean).length}</b>
        </Typography>
      </Stack>
    </Stack>
  )
}
