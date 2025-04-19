import ButtonsLayout from "../components/ButtonsLayout"
import GridDisplay from "../components/GridDisplay.tsx";


export default function ArtGalleryPage() {


  return (
    <div className="flex flex-col items-center min-h-screen p-4 bg-gray-50">
      <h1 className="text-3xl font-bold mb-2 text-gray-800">Art Gallery District</h1>
      <p className="text-gray-600 mb-6 text-center max-w-2xl">
          <h2>This is a fun game of "Gallery Rush".</h2>
          Try and win the game by extinct all galleries, get stuck in a static grid-state or enter a loop
      </p><br/>

      <ButtonsLayout />
      <GridDisplay />
    </div>
  )
}
