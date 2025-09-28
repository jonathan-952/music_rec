"use client"

import { useState, useRef, useEffect } from "react"
import { Play, Pause } from "lucide-react"

export interface Song {
  index: number
  title: string
  artist: string
  audio: string
}

interface AudioPlayerProps {
  song: Song
}

export function AudioPlayer({song}: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [progress, setProgress] = useState(0)
  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return


    const handleTimeUpdate = () => {
      if (audio.duration) {
        setProgress((audio.currentTime / audio.duration) * 100)
      }
    }

    audio.addEventListener("timeupdate", handleTimeUpdate)

    audio
      .play()
      .then(() => setIsPlaying(true))
      .catch(() => setIsPlaying(false))

    return () => {
      audio.removeEventListener("timeupdate", handleTimeUpdate)
    }
  }, [song.index])

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
          <h2 className="text-2xl font-bold text-white">{song.title}</h2>
          <p className="text-zinc-300 text-lg">{song.artist}</p>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-zinc-800 rounded-full h-1">
          <div
            className="bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 h-1 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Play/Pause */}
        <div className="flex items-center justify-center">
          <button
            onClick={togglePlayPause}
            className="rounded-full w-16 h-16 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:scale-105 transition-transform shadow-lg flex items-center justify-center"
          >
            {isPlaying ? <Pause className="w-6 h-6 text-white" /> : <Play className="w-6 h-6 ml-1 text-white" />}
          </button>
        </div>

        {/* Hidden Audio */}
        <audio ref={audioRef} src={song.audio} preload="metadata" />
      </div>
    </div>
  )
}