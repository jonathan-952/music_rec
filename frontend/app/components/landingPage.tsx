"use client"

import { useState } from "react"
import { Heart, Check, X} from "lucide-react"
import { AudioPlayer } from "@/components/audioPlayer"
import { Sidebar } from "@/components/likedSongs"
import axios from "axios"
import { useEffect } from "react"
import {Song} from '@/components/audioPlayer'

export default function LandingPage() {
  const [song, setSong] = useState<Song | null>(null);
  const [likedSongs, setLikedSongs] = useState([])
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [reroll, setReroll] = useState(0)


   useEffect(() => {
    const fetchSong = async () => {
      try {
        const res = await axios.get("http://184.72.148.78:8000/recommend-song");
        const liked = await axios.get("http://184.72.148.78:8000/liked-songs");
        setSong(res.data); // backend returns payload (metadata, index, etc)
        setLikedSongs(liked.data)
        
      } catch (err) {
        console.error("Error fetching song:", err);
      }
    };

      fetchSong()
    }, [reroll]);

    // add event listeners here so that whenever user likes/dislikes, fetch another song


  const handleFeedback = async (rating: number) => {
      try {
      await axios.post(`http://184.72.148.78:8000/feedback`, {
        rating: rating, 
        index: song!.index,
      });
      setReroll(prev => prev + 1);

    } catch (err) {
      console.error("Error submitting rating:", err);
    }
  };

  return (
    <main className="min-h-screen bg-black flex flex-col">
      <div className="flex justify-end p-7">
        <button
          onClick={() => setIsSidebarOpen(true)}
          className="p-3 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 hover:scale-105 hover:cursor-pointer transition-transform"
        >
          <Heart className="w-6 h-6 text-white" />
        </button>
      </div>

      <div className="flex-1 flex items-center justify-center px-6">
        <div className="w-full max-w-md space-y-6">
          {song && <AudioPlayer song={song} />}
          <div className="flex justify-center gap-20">
            <button
              onClick={() => handleFeedback(1)}
              className="flex justify-center px-6 py-3 w-25 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 hover:scale-105 hover:cursor-pointer transition-transform text-white font-medium"
            >
              <Check size={28} strokeWidth={2.5} />
            </button>
            <button
              onClick={() => handleFeedback(-1)}
              className="flex justify-center px-6 py-3 w-25 rounded-full bg-gradient-to-r from-purple-500  to-blue-500 hover:scale-105 hover:cursor-pointer transition-transform text-white font-medium"
            >
               <X size={28} strokeWidth={2.5} />
            </button>
          </div>
        </div>
      </div>

      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} likedSongs={likedSongs} />
    </main>
  )
}
