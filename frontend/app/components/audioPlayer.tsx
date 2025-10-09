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

export function AudioPlayer({ song }: AudioPlayerProps) {
  // Extract YouTube video ID (e.g. from https://www.youtube.com/watch?v=8779P4rim80)
  const videoIdMatch = song.audio.match(/(?:v=|\/)([0-9A-Za-z_-]{11})/)
  const videoId = videoIdMatch ? videoIdMatch[1] : null

  return (
    <div className="bg-zinc-900 rounded-2xl p-8 border border-zinc-800 shadow-2xl max-w-md mx-auto">
      <div className="space-y-6 text-center">
        {/* Song Info */}
        <h2 className="text-2xl font-bold text-white">{song.title}</h2>
        <p className="text-zinc-300 text-sm">{song.artist}</p>

        {/* YouTube Player */}
        {videoId ? (
          <div className="aspect-video rounded-xl overflow-hidden shadow-lg">
            <iframe
              src={`https://www.youtube.com/embed/${videoId}?autoplay=0&modestbranding=1&rel=0`}
              title={song.title}
              width="100%"
              height="100%"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        ) : (
          <p className="text-zinc-400">Invalid YouTube URL</p>
        )}
      </div>
    </div>
  )
}