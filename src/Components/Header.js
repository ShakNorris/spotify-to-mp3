import React from 'react'
import './Header.css'

function Header() {
  return (
    <div className='header'>
        <div className='head-items'>
            <img className="logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/2048px-Spotify_logo_without_text.svg.png" alt="Project Logo" />
            <h1>Spotify Downloader</h1>
        </div>
    </div>
  )
}

export default Header