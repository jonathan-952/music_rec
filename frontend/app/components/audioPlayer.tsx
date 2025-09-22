"use client"

import { useState, useRef, useEffect } from "react"
import { Play, Pause, SkipForward } from "lucide-react"

interface Song {
  id: number
  title: string
  artist: string
  album: string
  duration: string
  coverUrl: string
  audioUrl: string
}

interface AudioPlayerProps {
  song: Song
  onEnded: () => void
  onSkip: () => void
}

export function AudioPlayer({ song, onEnded, onSkip }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleEnded = () => {
      setIsPlaying(false)
      onEnded()
    }

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime)
    }

    const handleLoadedMetadata = () => {
      setDuration(audio.duration)
    }

    audio.addEventListener("ended", handleEnded)
    audio.addEventListener("timeupdate", handleTimeUpdate)
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
  }, [song.id, onEnded])

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

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0

  return (
    <div className="bg-zinc-900 rounded-2xl p-8 border border-zinc-800 shadow-2xl max-w-md mx-auto">
      <div className="space-y-6">
        {/* Song Info */}
        <div className="text-center space-y-3">
          <h2 className="text-2xl font-bold text-white text-balance">{song.title}</h2>
          <div className="space-y-1">
            <p className="text-zinc-300 text-lg">{song.artist}</p>
            <p className="text-zinc-400 text-sm">{song.album}</p>
          </div>
        </div>

        <div className="space-y-2">
          <div className="w-full bg-zinc-800 rounded-full h-1">
            <div
              className="bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 h-1 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
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

          <button
            onClick={onSkip}
            className="rounded-full w-12 h-12 bg-zinc-800 hover:bg-zinc-700 transition-colors flex items-center justify-center"
          >
            <SkipForward className="w-5 h-5 text-white" />
          </button>
        </div>

        {/* Hidden Audio Element */}
        <audio ref={audioRef} src={song.audioUrl} preload="metadata" />
      </div>
    </div>
  )
}
