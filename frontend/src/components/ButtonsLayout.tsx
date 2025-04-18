import { Button, Slider, Stack, Typography } from "@mui/material"
import { PlayArrow, Pause, Refresh, Replay, Close } from "@mui/icons-material"
import { useGrid } from "../providers/GridProvider"

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

  return (
    <Stack spacing={3} alignItems="center" width="100%">
      {/* Buttons */}
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
          {isPlaying ? "Pause" : "Play"} (Space)
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
          Active Galleries: <b>{grid.flat().filter(Boolean).length}</b>
        </Typography>
      </Stack>
    </Stack>
  )
}
