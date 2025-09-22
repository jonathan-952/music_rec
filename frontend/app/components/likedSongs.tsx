"use client"

import { X } from "lucide-react"
import { useEffect } from "react"
import axios from "axios"

interface Song {
  id: number
  title: string
  artist: string
  album: string
  duration: string
  coverUrl: string
  audioUrl: string
}

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
  likedSongs: Song[]
}


export function Sidebar({ isOpen, onClose, likedSongs }: SidebarProps) {
  if (!isOpen) return null

  

  return (
    <div className="fixed inset-0 z-50 flex">
      <div className="flex-1 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div className="w-80 bg-zinc-900 border-l border-zinc-800 p-6 overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-bold text-white">Liked Songs</h2>
          <button onClick={onClose} className="p-2 hover:bg-zinc-800 rounded-lg transition-colors">
            <X className="w-4 h-4 text-zinc-400" />
          </button>
        </div>

        {likedSongs.length === 0 ? (
          <p className="text-zinc-400 text-center py-8">No liked songs yet. Start discovering!</p>
        ) : (
          <div className="space-y-3">
            {likedSongs.map((song) => (
              <div key={song.id} className="p-3 bg-zinc-800/50 rounded-lg">
                <h3 className="font-medium text-sm text-white">{song.title}</h3>
                <p className="text-xs text-zinc-400">
                  {song.artist} • {song.album}
                </p>
                <p className="text-xs text-zinc-400 mt-1">{song.duration}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}