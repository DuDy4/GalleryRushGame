import { useGrid } from "../providers/GridProvider"
import { Box, Typography } from "@mui/material"

export default function GridDisplay() {
    const { grid, toggleCell, winReason, removeWinReason } = useGrid()

    if (!(grid && grid.length)) {
        return (
            <Box
                sx={{
                    p: 2,
                    border: "1px solid",
                    borderColor: "error.main",
                    borderRadius: 1,
                    textAlign: "center",
                }}
            >
                Grid is not initialized
            </Box>
        )
    }

    return (
        <Box
            sx={{
                position: "relative", // so we can absolutely-position the overlay
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                p: 2,
            }}
        >
            {/* Grid container */}
            <Box
                sx={{
                    display: "grid",
                    gridTemplateColumns: `repeat(${grid.length}, 1fr)`,
                    width: "90vmin",
                    height: "90vmin",
                    borderRadius: 2,
                    boxShadow: 3,
                    padding: 1,
                    overflow: "hidden",
                    backgroundColor: "grey.100",
                    gap: "1px",
                    opacity: winReason ? 0.4 : 1,
                    pointerEvents: winReason ? "none" : "auto", // optional: disable clicks when won
                    transition: "opacity 0.3s",
                }}
            >
                {grid.map((row, i) =>
                    row.map((cell, j) => (
                        <Box
                            key={`${i}-${j}`}
                            onClick={() => toggleCell(i, j)}
                            sx={{
                                backgroundColor: cell ? "success.main" : "white",
                                "&:hover": {
                                    backgroundColor: cell ? "success.dark" : "grey.200",
                                },
                                aspectRatio: "1 / 1",
                                width: "100%",
                                cursor: "pointer",
                                transition: "background-color 0.2s",
                            }}
                        />
                    ))
                )}
            </Box>

            {/* Win overlay */}
            {winReason && (

                <Box
                    onClick={removeWinReason}
                    sx={{
                        position: "absolute",
                        top: 14,
                        left: 14,
                        width: "85vmin",
                        height: "85vmin",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        alignSelf: "center",
                        backgroundColor: "rgba(255, 255, 255, 0.7)", // semi-transparent white
                        backdropFilter: "blur(3px)",
                        borderRadius: 2,
                        p: 4,
                        zIndex: 1,
                    }}
                >
                    <Typography variant="h4" align="center" color="success.main">
                        🎉 You won!<br /><br/>
                        <Typography variant="h6" component="div" color="text.secondary">
                            {winReason}
                        </Typography>
                    </Typography>
                </Box>
            )}
        </Box>
    )
}
