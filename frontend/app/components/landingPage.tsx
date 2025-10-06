"use client"

import { useState } from "react"
import { Heart } from "lucide-react"
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
        const res = await axios.get("http://54.90.150.96:8000/recommend-song");
        const liked = await axios.get("http://54.90.150.96:8000/liked-songs");
        setSong(res.data); // backend returns payload (metadata, index, etc)
        console.log(res.data)
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
      await axios.post(`http://54.90.150.96:8000/feedback`, {
        rating: rating, 
        song: song!.index,
      });
      setReroll(prev => prev + 1);

    } catch (err) {
      console.error("Error submitting rating:", err);
    }
  };

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
          {song && <AudioPlayer song={song} />}
          <div className="flex justify-center">
            <button
              onClick={() => handleFeedback(1)}
              className="px-6 py-3 rounded-full bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:scale-105 transition-transform text-white font-medium"
            >
              Like
            </button>
            <button
              onClick={() => handleFeedback(-1)}
              className="px-6 py-3 rounded-full bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:scale-105 transition-transform text-white font-medium"
            >
              Dislike
            </button>
          </div>
        </div>
      </div>

      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} likedSongs={likedSongs} />
    </main>
  )
}
