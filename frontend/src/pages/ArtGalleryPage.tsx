import { useEffect } from "react"
import ButtonsLayout from "../components/ButtonsLayout"
import { useGrid } from "../providers/GridProvider"
import GridDisplay from "../components/GridDisplay.tsx";

const GRID_SIZE = 20

export default function ArtGalleryPage() {
  const { grid, toggleCell, randomize, clear, step, togglePlay } = useGrid()

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
    <div className="flex flex-col items-center min-h-screen p-4 bg-gray-50">
      <h1 className="text-3xl font-bold mb-2 text-gray-800">Art Gallery District</h1>
      <p className="text-gray-600 mb-6 text-center max-w-2xl">
      </p>

      <ButtonsLayout />

          <div
              className="grid gap-[1px]"
              style={{
                  gridTemplateColumns: `repeat(${GRID_SIZE}, minmax(0, 1fr))`,
                  width: "fit-content",
              }}
          >
              <GridDisplay/>
          </div>
    </div>
  )
}
