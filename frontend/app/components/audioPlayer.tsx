"use client"

import { useState, useRef, useEffect } from "react"
import { Play, Pause, SkipForward } from "lucide-react"

interface Song {
  index: number
  title: string
  artist: string
}

interface AudioPlayerProps {
  song: Song
  onEnded: () => void
  onSkip: () => void
  onRate: (rating: number) => void
}

export function AudioPlayer({ song, onEnded, onSkip }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleEnded = () => {
      setIsPlaying(false)
      onEnded()
    }

    const handleLoadedMetadata = () => {
     
    }

    audio.addEventListener("ended", handleEnded)
    audio.addEventListener("loadedmetadata", handleLoadedMetadata)

    audio
      .play()
      .then(() => {
        setIsPlaying(true)
      })
      .catch(() => {
        // Auto-play failed, user needs to interact first
        setIsPlaying(false)
      })

    return () => {
      audio.removeEventListener("ended", handleEnded)
      audio.removeEventListener("timeupdate", handleTimeUpdate)
      audio.removeEventListener("loadedmetadata", handleLoadedMetadata)
    }
  }, [song.index, onEnded])

  const togglePlayPause = () => {
    const audio = audioRef.current
    if (!audio) return

    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }

  return (
    <div className="bg-zinc-900 rounded-2xl p-8 border border-zinc-800 shadow-2xl max-w-md mx-auto">
      <div className="space-y-6">
        {/* Song Info */}
        <div className="text-center space-y-3">
          <h2 className="text-2xl font-bold text-white text-balance">{song.title}</h2>
          <div className="space-y-1">
            <p className="text-zinc-300 text-lg">{song.artist}</p>
          </div>
        </div>

        <div className="space-y-2">
          <div className="w-full bg-zinc-800 rounded-full h-1">
            <div
              className="bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 h-1 rounded-full transition-all duration-300"
            />
          </div>
        </div>

        <div className="flex items-center justify-center gap-4">
          <button
            onClick={togglePlayPause}
            className="rounded-full w-16 h-16 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:scale-105 transition-transform shadow-lg flex items-center justify-center"
          >
            {isPlaying ? <Pause className="w-6 h-6 text-white" /> : <Play className="w-6 h-6 ml-1 text-white" />}
          </button>
        </div>

        {/* Hidden Audio Element */}
        <audio ref={audioRef} src={song.audio} preload="metadata" />
      </div>
    </div>
  )
}
