"use client"

import { useState } from "react"
import { Heart } from "lucide-react"
import { AudioPlayer } from "@/components/audioPlayer"
import { Sidebar } from "@/components/likedSongs"
import axios from "axios"
const sampleSongs = [
  {
    id: 1,
    title: "Midnight Dreams",
    artist: "Luna Eclipse",
    album: "Nocturnal Vibes",
    duration: "3:42",
    audioUrl: "/placeholder-audio.mp3",
  },
  {
    id: 2,
    title: "Electric Pulse",
    artist: "Neon Waves",
    album: "Digital Hearts",
    duration: "4:15",
    audioUrl: "/placeholder-audio.mp3",
  },
  {
    id: 3,
    title: "Ocean Breeze",
    artist: "Coastal Sounds",
    album: "Tidal Rhythms",
    duration: "3:28",
    audioUrl: "/placeholder-audio.mp3",
  },
]

export default function LandingPage() {
  const [currentSongIndex, setCurrentSongIndex] = useState(0)
  const [likedSongs, setLikedSongs] = useState([])
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const currentSong = sampleSongs[currentSongIndex]

  const handleSkip = () => {
    setCurrentSongIndex((prev) => (prev + 1) % sampleSongs.length)
  }

  const handleLike = () => {
    setLikedSongs((prev) => [...prev, currentSong])
  }

  return (
    <main className="min-h-screen bg-black flex flex-col">
      <div className="flex justify-end p-6">
        <button
          onClick={() => setIsSidebarOpen(true)}
          className="p-3 rounded-full bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:scale-105 transition-transform"
        >
          <Heart className="w-5 h-5 text-white" />
        </button>
      </div>

      <div className="flex-1 flex items-center justify-center px-6">
        <div className="w-full max-w-md space-y-6">
          <AudioPlayer song={currentSong} onSkip={handleSkip} />
          <div className="flex justify-center">
            <button
              onClick={handleLike}
              className="px-6 py-3 rounded-full bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:scale-105 transition-transform text-white font-medium"
            >
              Like
            </button>
          </div>
        </div>
      </div>

      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} likedSongs={likedSongs} />
    </main>
  )
}
