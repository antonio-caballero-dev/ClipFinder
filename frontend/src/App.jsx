import Sidebar from "./components/Sidebar";
import VideoPlayer from "./components/VideoPlayer";
import Consulta from "./components/Consulta";
import "./AppLayout.css";

import React, { useState } from "react";

function App() {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [consultaHabilitada, setConsultaHabilitada] = useState(false);
  const [clipsFound, setClipsFound] = useState(false);
  const [sidebarVisible, setSidebarVisible] = useState(true);
  // Recibe el estado de preparado desde Sidebar
  const handlePreparadoChange = (isReady) => {
    setConsultaHabilitada(isReady);
  };
  return (
    <div className="app-layout">
      {/* Sidebar */}
      {sidebarVisible && (
        <Sidebar
          selected={selectedVideo}
          setSelected={setSelectedVideo}
          onPreparadoChange={handlePreparadoChange}
        />
      )}
      {/* Botón para mostrar/ocultar sidebar */}
      <button
        className="sidebar-toggle-btn"
        style={{
          position: 'absolute',
          top: 18,
          left: sidebarVisible ? 420 : 0,
          zIndex: 10,
          background: '#1976d2',
          color: '#fff',
          border: 'none',
          borderRadius: '0 8px 8px 0',
          padding: '8px 12px',
          fontWeight: 700,
          fontSize: 18,
          boxShadow: '0 2px 8px #b3e5fc44',
          cursor: 'pointer',
          transition: 'left 0.2s',
        }}
        onClick={() => setSidebarVisible(v => !v)}
        title={sidebarVisible ? 'Ocultar menú' : 'Mostrar menú'}
      >
        {sidebarVisible ? '⟨' : '⟩'}
      </button>
      {/* Main content */}
      <div className="main-content">
        <div className="video-player">
          <VideoPlayer video={selectedVideo} className={clipsFound ? "video-player-element shrinked" : "video-player-element"} />
        </div>
        <div className="consulta">
          <Consulta consultaHabilitada={consultaHabilitada} selectedVideo={selectedVideo} onClipsChange={setClipsFound} />
        </div>
      </div>
    </div>
  );
}

export default App;
