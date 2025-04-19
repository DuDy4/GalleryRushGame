import { useGrid } from "../providers/GridProvider"
import { Box } from "@mui/material"

export default function GridDisplay() {
    const { grid, toggleCell } = useGrid()

    if (!grid.length) {
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

    const size = grid.length // assume square grid

    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                p: 2,
            }}
        >
            <Box
                sx={{
                    display: "grid",
                    gridTemplateColumns: `repeat(${size}, 1fr)`,
                    width: "90vmin",             // fills most of viewport, max square
                    height: "90vmin",
                    borderRadius: 2,
                    boxShadow: 3,
                    padding: 1,
                    overflow: "hidden",
                    backgroundColor: "grey.100",
                    gap: "1px",                   // spacing between cells
                }}
            >
                <>
                    {
                        grid.map((row, i) =>
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
                </>
            </Box>
        </Box>
    )
}
